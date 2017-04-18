import unittest
from numpy import array, allclose, random, cos, pi, sin
from numpy.fft import fft
from model_fft import ModelFFT


class TestModelFFT(unittest.TestCase):

    # def test_run2(self):
    #     model_fft = ModelFFT()
    #     model_fft.gen_radix_2(2)
    #     data = array([1, 10])
    #     result, _ = model_fft.run(data)
    #     answ = array([11, -9], dtype=complex)
    #     self.assertTrue(allclose(result, answ))
    #
    # def test_run4(self):
    #     model_fft = ModelFFT()
    #     model_fft.gen_radix_2(4)
    #     data = array([1, 10, 100, 1j])
    #     result, _ = model_fft.run(data)
    #     self.assertTrue(allclose(result, fft(data)))
    #
    # def test_run8(self):
    #     model_fft = ModelFFT()
    #     model_fft.gen_radix_2(8)
    #     data = array([1, 10, 100, 1000, 1j, 10j, 100j, 1000j])
    #     result, _ = model_fft.run(data)
    #     self.assertTrue(allclose(result, fft(data)))

    # def test_run(self):
    #     model_fft = ModelFFT()
    #     points = [16, 32, 64]
    #     flops = [176, 496, 1296]
    #     for i in range(3):
    #         n = points[i]
    #         model_fft.gen_radix_2(n)
    #         calc_flops = model_fft.calc_flops()
    #         data = random.sample(n)+1j*random.sample(n)
    #         result, _ = model_fft.run(data)
    #         self.assertTrue(allclose(result, fft(data)))
    #         self.assertEqual(flops[i], calc_flops)

    # def test_transfer(self):
    #     model_fft = ModelFFT()
    #
    #     model_fft.gen_radix_2(8)
    #     model_fft.transfer_up(1, 3, (1-1j)*cos(pi/4))
    #     data = array([1, 10, 100, 1000, 1j, 10j, 100j, 1000j])
    #     result, _ = model_fft.run(data)
    #     self.assertTrue(allclose(result, fft(data)))
    #
    #     n = 16
    #     model_fft.gen_radix_2(n)
    #     for i in range(3):
    #         angle = (i+1)*pi/8
    #         model_fft.transfer_up(1, 2*i+3, (sin(angle)-1j*cos(angle)))
    #     calc_flops = model_fft.calc_flops()
    #     data = random.sample(n) + 1j * random.sample(n)
    #     result, _ = model_fft.run(data)
    #     self.assertTrue(allclose(result, fft(data)))

    def test_minimize(self):
        model_fft = ModelFFT()
        for n in [16, 32, 64, 128, 256, 512, 1024]:
            model_fft.gen_radix_2(n)
            calc_flops_before = model_fft.calc_flops()
            model_fft.minimize_flops()
            calc_flops = model_fft.calc_flops()
            data = random.sample(n) + 1j * random.sample(n)
            result, _ = model_fft.run(data)
            self.assertTrue(allclose(result, fft(data)))
            print("point - ", n, "r2 - ", calc_flops_before, "opt - ", calc_flops)


if __name__ == '__main__':
    unittest.main()