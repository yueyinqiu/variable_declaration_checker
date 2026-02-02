class VariableScope:
    def __init__(self, 
                 parent: 'VariableScope | None',
                 is_class: bool, 
                 is_class_init: bool) -> None:
        self.__parent = parent
        self.__variables: set[str] = set()
        self.__is_class: bool = is_class
        self.__is_class_init: bool = is_class_init

    def is_class(self):
        return self.__is_class

    def is_class_init(self):
        return self.__is_class_init

    def assign_variable(self, name: str) -> bool:
        """
        :return: False indicates no problem. True indicates the variable has not been declared.
        :rtype: bool
        """
        if name == "_":
            return False

        if name in self.__variables:
            return False
        
        self.__variables.add(name)
        return True

    def declare_variable(self, name: str):
        """
        :return: False indicates no problem. True indicates the variable is declared twice.
        :rtype: bool
        """
        if name == "_":
            return False

        if name in self.__variables:
            return True
        
        self.__variables.add(name)
        return False

    def remove_variable(self, name: str):
        self.__variables.discard(name)

    def create_sub_scope(self, is_class: bool, is_init_function: bool):
        return VariableScope(self, is_class, self.__is_class and is_init_function)

    def get_parent_scope(self):
        assert self.__parent is not None
        return self.__parent
