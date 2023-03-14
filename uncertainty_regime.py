class uncertainty_regime:
    
    def __init__(self, p_0, base_earnings, growth, growth_prime, risk_pre, rfr, 
                 ir, perpetual_growth, perpetual_return):
        self.p_0 = p_0
        self.base_earnings = base_earnings
        self.growth = growth
        self.growth_prime = growth_prime
        self.risk_pre = risk_pre
        self.rfr = rfr
        self.ir = ir
        self.perpetual_growth = perpetual_growth
        self.perpetual_return = perpetual_return
    
    
    def get_discount_rate(self) -> float:
        return 1 / (1 + self.rfr + self.risk_pre)
    
    def get_perpetual_p(self) -> float:
        return 1 - self.perpetual_growth /self.perpetual_return
    
    def calculate_pv(self, n) -> float:
        """
        Calculates the present value using the derivation outlined in the
        previous part of Eigenthings 
        
        @params:
            n   - Required  : number of years out to calculate future cash flows
            (Int)
            
        """
        pv = 0
        earnings = self.base_earnings
        
        # begin by iterating over n-1 projected years in the future
        for i in range(1, n):
            earnings = earnings*(1 + self.growth_prime) if i == 1 else earnings*(1 + self.growth)
            new_p = self.p_0 + i * (self.get_perpetual_p() - self.p_0) / n
            cf = earnings * new_p
            pv += cf * self.get_discount_rate() ** i
        
        # calculate terminal value tv
        tv_num = earnings * (1 + self.perpetual_growth) * self.get_perpetual_p()
        tv_denom = (self.rfr + self.erp - self.perpetual_growth)
        tv =  tv_num / tv_denom
        
        # calculate the next year's cash flows CF_n
        pv_next = tv * self.get_discount_rate ** n
        
        return pv + pv_next
    
    
    def convert_p_to_growth(self, n, g_0, g_prime) -> float:
        """
        Calcualtes the conversion between percentage of cash flows retained and
        the growth rate using the derivation outlined in the previous part of
        Eigenthings 
        
        @params:
            n   - Required  : number of years out to calculate future cash flows
            (Int)
            
        """
        num = -1 * (1 + self.p * (g_prime - g_0))
        denom = (1 + g_0) * (1 + g_prime) ** (n - 1)
        return (num / denom)**(1/n)
    
    def total_valuation(self) -> float:
        return       