from numpy import zeros, log2, array, ndarray, hstack, vstack, exp, pi, isclose


class ModelFFT:
    w_factors = zeros(1)
    permutations = zeros(1)

    def b(self, data):
        result = zeros(data.shape, dtype=complex)
        n = data.size
        for i in range(n // 2):
            j = i + n // 2
            result[i] = data[i] + data[j]
            result[j] = data[i] - data[j]
        return result

    def p(self, data, perm):
        result = zeros(data.shape, dtype=complex)
        n = data.size
        for i in range(n):
            result[i] = data[perm[i]]
        return result

    def w(self, data, w_factor):
        return data * w_factor

    def run(self, data):
        stages, points = self.permutations.shape
        assert (stages, points) == self.w_factors.shape
        assert points == data.size

        result = zeros((stages + 1, points), dtype=complex)
        result[0] = data
        for i in range(stages - 1):
            step1 = self.w(result[i], self.w_factors[i])
            step2 = self.p(step1, self.permutations[i])
            result[i + 1] = self.b(step2)
        step1 = self.w(result[stages - 1], self.w_factors[stages - 1])
        result[stages] = self.p(step1, self.permutations[stages - 1])

        return result[stages], result

    # region Radix 2 generation
    def gen_radix_2(self, n):
        if n == 2:
            self.w_factors = array([[1, 1], [1, 1]], dtype=complex)
            self.permutations = array([[0, 1], [0, 1]], dtype=int)
            return self
        else:
            half_model = ModelFFT()
            half_model.gen_radix_2(n // 2)
            self.permutations = vstack(
                (array([i for i in range(n)]), self.__clue_p(self.__union_p(
                    half_model.permutations, half_model.permutations))))
            self.w_factors = vstack(
                (zeros(n, dtype=complex) + 1, self.__clue_w(self.__union_w(
                    half_model.w_factors, half_model.w_factors))))
            return self

    @staticmethod
    def __union_p(p1, p2):
        s, n2 = p1.shape
        n = n2 * 2
        result = zeros((s, n), dtype=int)
        for i in range(n2):
            result[:, 2 * i] = p1[:, i] * 2
            result[:, 2 * i + 1] = p2[:, i] * 2 + 1
        return result

    @staticmethod
    def __clue_p(p):
        _, n = p.shape
        result = p.copy()
        pp = zeros(n)
        for i in range(n // 2):
            pp[2 * i] = i
            pp[2 * i + 1] = i + n // 2
        for i in range(n):
            result[0, i] = pp[p[0, i]]
        return result

    @staticmethod
    def __union_w(w1, w2):
        s, n2 = w1.shape
        n = n2 * 2
        result = zeros((s, n), dtype=complex)
        for i in range(n2):
            result[:, 2 * i] = w1[:, i]
            result[:, 2 * i + 1] = w2[:, i]
        return result

    @staticmethod
    def __clue_w(w):
        _, n = w.shape
        result = w.copy()
        ww = hstack((
            array([1 for i in range(n // 2)]),
            array([exp(-2j * pi * i / n) for i in range(n // 2)])))
        result[0, :] = result[0, :] * ww
        return result

    # endregion
    # region FLOPs calculator
    def calc_flops(self):
        s, n = self.w_factors.shape
        sum = 0
        for i in range(s):
            for j in range(n):
                sum += self.__flops(self.w_factors[i, j])
        return sum + 2 * (s - 1) * n

    @staticmethod
    def __flops(x):
        if isclose(x.real, 0):
            if isclose(abs(x.imag), 1):
                return 0
            else:
                return 2
        if isclose(x.imag, 0):
            if isclose(abs(x.real), 1):
                return 0
            else:
                return 2
        if isclose(abs(x.real), 1):
            if isclose(abs(x.imag), 1):
                return 2
            else:
                return 4
        if isclose(abs(x.imag), 1):
            return 4
        if isclose(abs(x.real), abs(x.imag)):
            return 4
        return 6

    # endregion

    def transfer_up(self, stage, butterfly, factor):
        s, n = self.w_factors.shape
        self.w_factors[stage, self.permutations[stage, butterfly]] *= factor
        self.w_factors[stage, self.permutations[stage, butterfly+n//2]] *= factor
        self.w_factors[stage+1, butterfly] /= factor
        self.w_factors[stage+1, butterfly+n//2] /= factor

    def __eval_transfer(self, stage, butterfly):
        s, n = self.w_factors.shape
        w1 = self.w_factors[stage, self.permutations[stage, butterfly]]
        w2 = self.w_factors[stage, self.permutations[stage, butterfly+n//2]]
        w3 = self.w_factors[stage+1, butterfly]
        w4 = self.w_factors[stage+1, butterfly+n//2]
        before_cost = self.__flops(w1)+self.__flops(w2)\
                      +self.__flops(w3)+self.__flops(w4)
        factor = 1/w1
        w1 *= factor
        w2 *= factor
        w3 /= factor
        w4 /= factor
        post_cost = self.__flops(w1)+self.__flops(w2)\
                      +self.__flops(w3)+self.__flops(w4)
        if post_cost<before_cost:
            return True, factor
        else:
            return False, 0

    def minimize_flops(self):
        s, n = self.w_factors.shape
        for stage in range(s-1):
            for butterfly in range(n//2):
                right, factor = self.__eval_transfer(stage, butterfly)
                if right:
                    self.transfer_up(stage, butterfly, factor)