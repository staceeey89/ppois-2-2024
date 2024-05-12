class Feedback:
    
    def __init__(self) -> None:
        self.__feedback = []
        
    def getFeedbacks(self) -> list:
        return self.__feedback
            
    def addFeedback(self, feedback: str) -> None:
        self.__feedback.append(feedback)

