from geant4_pybind import *

#from particle import Particle
#particle = Particle.from_pdgid(pdgid)
#mass = particle.mass

class SteppingAction(G4UserSteppingAction):

  def __init__(self, app):
    super().__init__()
    self.app  = app
    self.data_buffer = app.data_buffer
    n = 1.35
    self.cerenkov_threshold_factor = 1./(1.-n**2)
    # E_th = mc^2 / sqrt(1-1/n^2),
    # where n = 1.35 for water, so 1/sqrt(1-1/n^2) = 1.4885
    #   for e+/e- E_th = 760 keV
    #   for mu    E_th = 157 MeV


  def UserSteppingAction(self, aStep):
    aTrack = aStep.GetTrack()
    particle = aTrack.GetDefinition()
    pdgid = particle.GetPDGEncoding()
    uid = aTrack.GetTrackID()
    parent_uid = aTrack.GetParentID()
    pre_step_point = aStep.GetPreStepPoint()
    post_step_point = aStep.GetPostStepPoint()
    position = post_step_point.GetPosition()/m
    time = post_step_point.GetGlobalTime()/ns
    momentum = post_step_point.GetMomentum()/GeV
    #Etot1 = post_step_point.GetTotalEnergy()/GeV
    Ekin1 = pre_step_point.GetKineticEnergy()/GeV
    Etot2 = post_step_point.GetTotalEnergy()/GeV
    #Ekin2 = post_step_point.GetKineticEnergy()/GeV
    # Save every track point 
    if Ekin1 > self.app.E_skip_min:
      self.data_buffer.tracks[uid].AddPoint([position.x, position.y, position.z, time, 
                                             momentum.x, momentum.y, momentum.z, Etot2] )
