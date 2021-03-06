from subprocess import check_output
import numpy
import sys 
import unittest

class SignalAudio:
    """
    Class Signal Audio who processes the recording retrieved by the Nao Robot
    """
    def __init__(self):
        self.__sample_rate = 48000 # KHz of the .wav file from robot NAO
        self.__fingerprint_source = [] # original whistle sound digitalized
        self.__fingerprint_target = [] # sound receive by the robot digitalized

        
        self.__span = 4 # number of points to scan cross correlation over (basically it's 150 but doesn't work because < len(ofWhistleSound))
        
        self.__step = 1 # step size (in points) of cross correlation

        self.__min_overlap = 4 # minimum number of points that must overlap in cross correlation /exception is raised if this cannot be met

        self.__threshold = 0.5 # report match when cross correlation has a peak exceeding threshold
        
    def getFingerprint_source(self):
        return self.__fingerprint_source
    
    def getFingerprint_target(self):
        return self.__fingerprint_target
    
    def correlate(self, source, target):
        """
        Initialise the sound receive by the robot (target) and the original whistle sound (source)
        """
        self.__fingerprint_source = self.__calculate_fingerprints(source)
        self.__fingerprint_target = self.__calculate_fingerprints(target)

        corr = self.__compare(self.__fingerprint_source, self.__fingerprint_target)
        max_corr_offset = self.__get_max_corr(corr, source, target)

        return max_corr_offset
    
    def __calculate_fingerprints(self, filename):
        """
        The audio file is digitized into a list of integer after being sampled at a particular sample rate
        """
        try:
            fpcalc_out = check_output('fpcalc -raw -length %i %s'
                                            % (self.__sample_rate, filename), shell=True)
        except Exception,e:
            print "One of the audio file is too short."
            sys.exit(1)

        fingerprint_index = fpcalc_out.find('FINGERPRINT=') + 12

        # convert fingerprint to list of integers
        fingerprints = map(int, fpcalc_out[fingerprint_index:].split(','))
        
        return fingerprints

    def __correlation(self, listx, listy):
        """
        We do not directly compare all the fingerprints of listx and listy. We compare corresponding fingerprints in both lists.
        If the difference between fingerprint (covariance) bits is unto 1, it is safe to assume that the fingerprints are similar.
        More the covariance is low, more the similarity of the 2 list low too and vice versa.
        """
        if len(listx) == 0 or len(listy) == 0:
            # Error checking in main program should prevent us from ever being able to get here.
            raise Exception('Empty lists cannot be correlated.')
        if len(listx) > len(listy):
            listx = listx[:len(listy)]
        elif len(listx) < len(listy):
            listy = listy[:len(listx)]
        
        covariance = 0
        for i in range(len(listx)):
            covariance += 32 - bin(listx[i] ^ listy[i]).count("1")
        covariance = covariance / float(len(listx))
        
        return covariance/32

    def __cross_correlation(self, listx, listy, offset):
        """
        Return cross correlation, with listy offset from listx
        """
        if offset > 0:
            listx = listx[offset:]
            listy = listy[:len(listx)]
        elif offset < 0:
            offset = -offset
            listy = listy[offset:]
            listx = listx[:len(listy)]
        if min(len(listx), len(listy)) < self.__min_overlap:
            # Error checking in main program should prevent us from ever being able to get here.
            return None
        #raise Exception('Overlap too small: %i' % min(len(listx), len(listy)))
        return self.__correlation(listx, listy)

    def __compare(self, listx, listy):
        """
        Cross correlate listx and listy with offsets from -span to span
        """
        if self.__span > min(len(listx), len(listy)):
            # Error checking in main program should prevent us from ever being able to get here.
            raise Exception('span >= sample size: %i >= %i\n'
                            % (self.__span, min(len(listx), len(listy)))
                            + 'Reduce span, reduce crop or increase sample_time.')
        corr_xy = []
        for offset in numpy.arange(-self.__span, self.__span + 1, self.__step):
            corr_xy.append(self.__cross_correlation(listx, listy, offset))
        return corr_xy

    def __max_index(self, listx):
        """
        Return index of maximum value in list
        """
        max_index = 0
        max_value = listx[0]
        for i, value in enumerate(listx):
            if value > max_value:
                max_value = value
                max_index = i
        return max_index
  
    def __get_max_corr(self, corr, source, target):
        """
        Return the result of the match.
        If True then the sound source is similar to the target audio source.
        Else return False then the sound source is not similar to the target audio source
        """
        max_corr_index = self.__max_index(corr)
        max_corr_offset = -self.__span + max_corr_index * self.__step
        print "max_corr_index = ", max_corr_index, "max_corr_offset = ", max_corr_offset
        # report matches
        if corr[max_corr_index] > self.__threshold:
            print('%s and %s match with correlation of %.4f at offset %i'
                % (source, target, corr[max_corr_index], max_corr_offset)) 
            return True
        else:
            print ("The covariance is %.4f < 0.5, it seem that is not the same sound"%(corr[max_corr_index]))
            return False

class TestSignalAudio(unittest.TestCase):

    def test_correlate_return_true(self):
        """
        Test the correlation with the exactly same audio
        """
        s1 = SignalAudio()

        self.assertTrue(s1.correlate("whistle-3sec.wav","whistle-3sec.wav"))

    def test_correlate_return_true2(self):
        """
        Test the correlation with 2 different audios with similarity
        """
        s1 = SignalAudio()

        self.assertTrue(s1.correlate("whistle-3sec.wav","other_whistle.wav"))

    def test_correlate_return_false(self):
        """
        Test the correlation with 2 different audios with no similarity
        """
        s1 = SignalAudio()

        self.assertFalse(s1.correlate("whistle-3sec.wav","Dog-test.wav"))

    def test_correlate_RaisesIllegalArguments(self):
        """
        Raise an exception for the correlate method when I pass illegals arguments
        """
        s1 = SignalAudio()

        self.assertRaises(Exception, s1.correlate, ("je veux une erreur de parametre", None, "Erreur"))

    def test_correlate_with_no_arguments(self):
        """
        Raise an exception for the correlate method when I pass no arguments to the function
        """
        s1 = SignalAudio()

        self.assertRaises(Exception, s1.correlate)

if __name__ == "__main__":

    unittest.main()