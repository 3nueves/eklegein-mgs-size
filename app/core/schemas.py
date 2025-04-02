"""user schema"""

from abc import ABC, abstractmethod

class Schemas(ABC):
    """user schema"""
    @abstractmethod
    def query(self, archetype: str, score: str) -> str:
        """query"""

class QueryUserCountry(Schemas):
    """query user and country"""

    def query(self, archetype: str, score: str) -> str:
        """Busca usuarios y sus nacionalidades"""

        query = f"""query userQuery($uid:string, $country:string){{
                user(func: uid($uid)){{
                User.name
                User.surname
                User.email
                uid
                tags
                country
                sector
                join_to_team
                chats{{
                    uid
                    Chat_users
                    Chat_name
                    Chat_messages{{
                        uid
                        Message_content
                    }}
                }}
                discarded_groups
                groups{{
                    uid
                #     Group.name
                #     Group.users{{
                #         uid
                #         User.email
                #     }}
                }}
                {archetype}{{
                    Archetype.name
                    ~relations{{
                        Archetype.name
                        ~{archetype}(orderdesc: {score}, first:20) @filter(eq(country, $country) and NOT eq(join_to_team, "Blocked") and NOT eq(join_to_team, "OnHold")) {{
                            uid
                            User.name
                            User.email
                            {score}
                            sector
                            join_to_team
                            country
                            discarded_groups
                            # {archetype}{{
                            #     Archetype.name  
                            # }}
                            groups{{
                                uid
                            }}
                        }}
                    }}
                }}
            }}
        }}"""
        return query

class QueryUserCountryUser(Schemas):
    """query user to user"""

    def query(self, archetype: str, score:str) -> str:
        """Busca usuarios y sus nacionalidades"""
        query = f"""query userQuery($uid:string, $country:string, $uid_second:string){{
                user(func: uid($uid)){{
                User.name
                User.surname
                User.email
                uid
                tags
                country
                sector
                join_to_team
                chats{{
                    uid
                    Chat_users
                    Chat_name
                    Chat_messages{{
                        uid
                        Message_content
                    }}
                }}
                discarded_groups
                groups{{
                    uid
                #     Group.name
                #     Group.users{{
                #         uid
                #         User.email
                #     }}
                }}
                {archetype}{{
                    Archetype.name
                    ~relations{{
                        Archetype.name
                        ~archetype_hard(orderdesc: score_hard) @filter(eq(country, $country) and uid($uid_second)) {{
                            uid
                            User.name
                            User.email
                            score_hard
                            sector
                            join_to_team
                            country
                            discarded_groups
                            groups{{
                                uid
                            }}
                        }}
                        ~archetype_medium(orderdesc: score_medium) @filter(eq(country, $country) and uid($uid_second)) {{
                            uid
                            User.name
                            User.email
                            score_medium
                            sector
                            join_to_team
                            country
                            discarded_groups
                            groups{{
                                uid
                            }}
                        }}
                        ~archetype_soft(orderdesc: score_soft) @filter(eq(country, $country) and uid($uid_second)) {{
                            uid
                            User.name
                            User.email
                            score_soft
                            sector
                            join_to_team
                            country
                            discarded_groups
                            groups{{
                                uid
                            }}
                        }}
                    }}
                }}
            }}
        }}"""
        return query

class ManageSchemas:
    """manage schema"""
    def __init__(self) -> None:
        self.operations = {}

    def load_querys(self, name, operation: Schemas):
        """query"""
        self.operations[name] = operation

    def exec_query(self, name: str, arch: str, score: str) -> str:
        """execute query"""
        # Como lo estamos llamando como método de clase le pasamos self.
        return self.operations[name].query(arch, score)
