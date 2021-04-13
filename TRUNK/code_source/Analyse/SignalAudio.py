from subprocess import check_output
import numpy
import sys 

class SignalAudio():
    def __init__(self):
        self.__sample_rate = 48000 
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
        self.__fingerprint_source = self.calculate_fingerprints(source)
        self.__fingerprint_target = self.calculate_fingerprints(target)

        corr = self.compare(self.__fingerprint_source, self.__fingerprint_target)
        print corr
        max_corr_offset = self.get_max_corr(corr, source, target)
    
    def calculate_fingerprints(self, filename):
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

    def correlation(self, listx, listy):
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

    def cross_correlation(self, listx, listy, offset):
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
        return self.correlation(listx, listy)

    def compare(self, listx, listy):
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
            corr_xy.append(self.cross_correlation(listx, listy, offset))
        return corr_xy

    def max_index(self, listx):
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
  
    def get_max_corr(self, corr, source, target):
        """
        Return the result of the match
        """
        max_corr_index = self.max_index(corr)
        max_corr_offset = -self.__span + max_corr_index * self.__step
        print "max_corr_index = ", max_corr_index, "max_corr_offset = ", max_corr_offset
        # report matches
        if corr[max_corr_index] > self.__threshold:
            print('%s and %s match with correlation of %.4f at offset %i'
                % (source, target, corr[max_corr_index], max_corr_offset)) 
        else:
            print "The covariance is under 0.5, it's seem that is not the same sound"


s1 = SignalAudio()
s1.correlate("whistle-3sec.wav","Dog-test.wav")
