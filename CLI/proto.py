class CountryState:
    def __init__(self):
        
        # economic policies
        self.economic_ideology = 50 # liberarian - state control
        self.taxation = {
            "low": 10,
            "medium": 30,
            "high": 60
        }

        # inside politics policy
        self.authoritarianism = 50 # direct democracy - power of one
        self.censorship = 70 # preventive censorship - complete freedom of speech

        # internal people policy
        self.social_policy = 50 # welfare state - minimum state

        # foreign policy
        self.diplomatic_ideology = 50 # peace - aggresive
        
        # culture
        self.culture_policy = 50 # culture - technocracy/utilatarianism
        self.religion_influence = 0 # secular - theocratic
        self.nationalism = 50 # cosmopolitanism - nationalism


        #environment
        self.green_policy = 50 # environmentalism - industry over all
        



        # stats/effects on country
        self.polarisation = 50
        self.terrorism = 50
        self.criminality = 50
        self.organised_crime = 50
        self.human_rights = 100




        self.foreign_policy = 50
        
        self.integrationism = 50


    def get_main_metrics(self):
        return {
            "economy": self.economic_ideology,
            "security": self.social_policy,
            "": self.diplomatic_ideology,
            "authoritarianism": self.authoritarianism,
            "green_policy": self.green_policy,
        }
