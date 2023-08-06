from geant4_pybind import *
import numpy as np

class StackingAction(G4UserStackingAction):

  def __init__(self, app):
    super().__init__()
    self.app = app
    self.data_buffer = app.data_buffer
    self.E_init = app.E_init
    self.ph_suppression_factor = app.ph_suppression_factor
    # Cherenkov threshold
    n = 1.35
    self.cerenkov_threshold_factor = 1./(1.-n**2)
    # E_th = mc^2 / sqrt(1-1/n^2),
    # where n = 1.35 for water, so 1/sqrt(1-1/n^2) = 1.4885
    #   for e+/e- E_th = 760 keV
    #   for mu    E_th = 157 MeV

  def ClassifyNewTrack(self, track):
    # If /process/optical/cerenkov/setTrackSecondariesFirst is set to True
    # then tracks are stacked even in the middle of their life,
    # so this method is invoked not only on particle creation.
    # This is temporary used to skip particles based on their energy,
    # because the possibility to kill particle in Stepping action is not 
    # yet available (G4Track.SetTrackStatus() is not yet pythonized).
    uid = track.GetTrackID()
    parentuid = track.GetParentID()
    position = track.GetPosition()/m
    time = track.GetGlobalTime()/ns
    pdgid = track.GetDefinition().GetPDGEncoding()
    momentum = track.GetMomentum()/GeV
    Etot = track.GetTotalEnergy()/GeV
    Ekin = track.GetKineticEnergy()/GeV
    # 
    # = Primary particles =======================
    #
    if uid == 1 and track.GetCurrentStepNumber() == 0: # only initial event vertex
      self.ph_suppression_factor = self.app.ph_suppression_factor
      self.app.E_init = Ekin
      self.app.E_skip_min = self.app.skip_min
      self.app.E_skip_max = self.app.skip_max
      if self.app.skip_mode == "fraction":
        self.app.E_skip_min *= self.app.E_init
        self.app.E_skip_max *= self.app.E_init
      #self.data_buffer.AddVertex([ [position.x, position.y, position.z, time],
      #                             [], 
      #                             [[pdgid, momentum.x, momentum.y, momentum.z, Etot]] ] )
      if track.GetCurrentStepNumber() == 0:
        self.data_buffer.CreateTrack(uid, parentuid, pdgid)
      self.data_buffer.tracks[uid].AddPoint([position.x, position.y, position.z, time, 
                                             momentum.x, momentum.y, momentum.z, Etot])
      particle_name = track.GetDefinition().GetParticleName()
      energy_sting = G4BestUnit(Ekin*GeV, "Energy")
      x,y,z = position.x, position.y, position.z
      px, py, pz = momentum.x, momentum.y, momentum.z
      pmag = np.sqrt(px**2+py**2+pz**2)
      px, py, pz = px/pmag, py/pmag, pz/pmag
      self.app.log.info(f"{particle_name}:  Ekin={energy_sting}  position=({x:.1f}, {y:.1f}, {z:.1f}) m\
  direction=({px:.1f}, {py:.1f}, {pz:.1f}) ")
    #
    # = Photons =================================
    #
    # - Store info and kill
    #
    if track.GetDefinition() == G4OpticalPhoton.OpticalPhoton():
      if self.app.ph_counter%self.ph_suppression_factor == 0:
        position = track.GetPosition()/m
        direction = track.GetMomentumDirection()/GeV
        time = track.GetGlobalTime()/ns
        wavelength = 1.23984193*1.e-6/Etot # in nm
        ph = np.array([position.x, position.y, position.z,
                       time,
                       direction.x, direction.y, direction.z,
                       wavelength])
        self.data_buffer.AddPhoton(ph)
        #if parentuid != 1: print(f"{time:.4f} photon    parent uid: {parentuid}")
      self.app.ph_counter += 1
      return G4ClassificationOfNewTrack.fKill
    #
    # - For secondary e+/e- store vertex and kill if E_skip_min < Etot < E_skip_max
    #
    if uid !=1 and track.GetDefinition() in [G4Electron.Electron(), G4Positron.Positron()]:
      if Ekin > self.app.E_skip_min and Ekin < self.app.E_skip_max:
        self.app.data_buffer.AddVertex([ [position.x, position.y, position.z, time],
                                         [], 
                                         [[pdgid, momentum.x, momentum.y, momentum.z, Etot]] ] )
        #print(f"{time:.4f}   = to kill =    uid: {uid},  parent uid: {parentuid}, {pdgid}, energy: {Ekin:.4f}")
        return G4ClassificationOfNewTrack.fKill
    #
    # - For all particles below Cherenkov: kill
    #
    mass = track.GetDefinition().GetPDGMass()/GeV
    if Etot < self.cerenkov_threshold_factor * mass:
      return G4ClassificationOfNewTrack.fKill
    #
    # - For survived particles store track points
    if track.GetCurrentStepNumber() == 0:
      self.data_buffer.CreateTrack(uid, parentuid, pdgid)
    self.data_buffer.tracks[uid].AddPoint([position.x, position.y, position.z, time, 
                                           momentum.x, momentum.y, momentum.z, Etot])
    # 
    return G4ClassificationOfNewTrack.fUrgent
