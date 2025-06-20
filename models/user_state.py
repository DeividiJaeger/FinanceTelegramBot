class UserStateManager:
    def __init__(self):
        self.user_states = {}
    
    def set_state(self, user_id, state_data):
        """Define o estado para um usuário."""
        self.user_states[user_id] = state_data
    
    def get_state(self, user_id):
        """Obtém o estado atual do usuário."""
        return self.user_states.get(user_id)
    
    def clear_state(self, user_id):
        """Remove o estado de um usuário."""
        if user_id in self.user_states:
            del self.user_states[user_id]
            return True
        return False
    
    def has_state(self, user_id):
        """Verifica se o usuário tem um estado definido."""
        return user_id in self.user_states
