class EventManager:
    '''
    It coordinate communication between the Model, View, and Controller.
    Model, View, and Controller are all listeners, the EventManager will broadcast an event to them by post()
    '''
    def __init__(self):
        self.listeners = []

    def register_listener(self, listener):
        '''
        Adds a listener to our spam list.
        It will receive Post()ed events through it's notify(event) call.
        '''
        self.listeners.append(listener)

    def unregister_listener(self, listener):
        '''
        Remove a listener from our spam list.
        This is implemented but hardly used.
        Our weak ref spam list will auto remove any listeners who stop existing.
        '''
        pass

    def post(self, event):
        '''
        Post a new event to the message queue.
        It will be broadcast to all listeners.
        '''
        # # this segment use to debug
        # if not (isinstance(event, Event_EveryTick) or isinstance(event, Event_EverySec)):
        #     print( str(event) )
        for listener in self.listeners:
            listener.notify(event)


class BaseEvent:
    '''
    A superclass for any events that might be generated by
    an object and sent to the EventManager.
    '''
    name = 'Generic event'
    def __init__(self):
        pass

    def __str__(self):
        # For Debug
        return self.name


class EventInitialize(BaseEvent):
    name = 'Initialize event'


class EventQuit(BaseEvent):
    name = 'Quit event'


class EventStateChange(BaseEvent):
    name = 'StateChange event'

    def __init__(self, state):
        self.state = state

    def __str__(self):
        return f'{self.name} => StateTo: {self.state}'


class EventEveryTick(BaseEvent):
    name = 'Tick event'


class EventTimesUp(BaseEvent):
    name = "Time's Up event"


class EventPlayerMove(BaseEvent):
    name = 'PlayerMove event'

    def __init__(self, player_id, direction):
        self.player_id = player_id
        self.direction = direction

    def __str__(self):
        return f'{self.name} => player_id {self.player_id} move {self.direction}'

class EventPlayerAttack (BaseEvent):
    name = 'PlayerAttack event'

    def __init__(self, player_id):
        self.player_id = player_id

    def __str__(self):
        return f'{self.name} => player_id {self.player_id} attack'

class EventPlayerSpecialAttack (BaseEvent):
    name = 'PlayerSpecialAttack event'

    def __init__(self, player_id):
        self.player_id = player_id

    def __str__(self):
        return f'{self.name} => player_id {self.player_id} special attack'

class EventToggleFullScreen(BaseEvent):
    name = 'ToggleFullScreen event'

class EventStop(BaseEvent):
    name = 'GameStop event'
    '''
    game stop and model stage change to STATE_STOP
    '''

class EventContinue(BaseEvent):
    name = 'GameContinue event'
    '''
    game continue and model stage change to STATE_PLAY
    '''

class EventRestart(BaseEvent):
    name = 'GameContinue event'
    '''
    game restart and model stage change to STATE_MENU
    '''

class EventHelloWorld(BaseEvent):
    name = 'Hello World event'
    '''
    hello world triggered
    '''

class EventBeAttacked(BaseEvent):
    name = 'player be special attack event'
    '''
    notify view player be special attacked
    '''
    def __init__(self, player_id):
        self.player_id = player_id

class EventSpecialAttackMovement(BaseEvent):
    name = 'player special attack success and show movement'
    '''
    notify view player special attack & its type
    '''

    def __init__(self, player_id, attack_type):
        self.player_id = player_id
        self.attack_type = attack_type

class EventGetProp(BaseEvent):
    name = 'player get prop'
    '''
    notify view player get prop
    '''

    def __init__(self, player_id, item_type):
        self.player_id = player_id
        self.item_type = item_type