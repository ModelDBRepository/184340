'''
Defines a class, Neuron473871592, of neurons from Allen Brain Institute's model 473871592

A demo is available by running:

    python -i mosinit.py
'''
class Neuron473871592:
    def __init__(self, name="Neuron473871592", x=0, y=0, z=0):
        '''Instantiate Neuron473871592.
        
        Parameters:
            x, y, z -- position offset
            
        Note: if name is not specified, Neuron473871592_instance is used instead
        '''
        
        # load the morphology
        from load_swc import load_swc
        load_swc('Rbp4-Cre_KL100_Ai14_IVSCC_-175331.06.01.01_469953750_m.swc', self,
                 use_axon=False, xshift=x, yshift=y, zshift=z)

        # custom axon (works because dropping axon during import)
        from neuron import h
        self.axon = [h.Section(cell=self, name='axon[0]'),
                     h.Section(cell=self, name='axon[1]')]
        for sec in self.axon:
            sec.L = 30
            sec.diam = 1
            sec.nseg = 1
        self.axon[0].connect(self.soma[0](0.5))
        self.axon[1].connect(self.axon[0](1))
        self.all += self.axon
        
        self._name = name
        self._insert_mechanisms()
        self._discretize_model()
        self._set_mechanism_parameters()
    
    def __str__(self):
        if self._name is not None:
            return self._name
        else:
            return "Neuron473871592_instance"
                
    def _insert_mechanisms(self):
        from neuron import h
        for sec in self.all:
            sec.insert("pas")
        for mech in [u'CaDynamics', u'Ca_HVA', u'Ca_LVA', u'Ih', u'Im', u'K_P', u'K_T', u'Kv3_1', u'NaTs', u'Nap', u'SK']:
            self.soma[0].insert(mech)
    
    def _set_mechanism_parameters(self):
        from neuron import h
        for sec in self.all:
            sec.Ra = 100.0
            sec.e_pas = -85.204750061
        for sec in self.apic:
            sec.cm = 2.0
            sec.g_pas = 0.000313701962891
        for sec in self.axon:
            sec.cm = 1.0
            sec.g_pas = 0.00076016120237
        for sec in self.dend:
            sec.cm = 2.0
            sec.g_pas = 9.96045940202e-05
        for sec in self.soma:
            sec.cm = 1.0
            sec.ena = 53.0
            sec.ek = -107.0
            sec.gbar_Im = 0.00134083
            sec.gbar_Ih = 5.5177e-05
            sec.gbar_NaTs = 0.342698
            sec.gbar_Nap = 0.000807581
            sec.gbar_K_P = 0.0520027
            sec.gbar_K_T = 0.00230792
            sec.gbar_SK = 0.000122074
            sec.gbar_Kv3_1 = 0.0112769
            sec.gbar_Ca_HVA = 0.000967165
            sec.gbar_Ca_LVA = 0.00680875
            sec.gamma_CaDynamics = 0.000773421
            sec.decay_CaDynamics = 430.696
            sec.g_pas = 0.000383038
    
    def _discretize_model(self):
        for sec in self.all:
            sec.nseg = 1 + 2 * int(sec.L / 40)

