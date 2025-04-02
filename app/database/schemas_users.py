"""user schema"""

class UserSchema:
    """users schema"""
    def query_user_country(self, archetype: str, score:str) -> str:
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


    def query_user_country_user(self, archetype: str, score:str) -> str:
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
                        # ~{archetype}(orderdesc: {score}, first:20) @filter(eq(country, $country) and uid($uid_second) and NOT eq(join_to_team, "Blocked") and NOT eq(join_to_team, "OnHold")) {{
                        ~{archetype}(orderdesc: {score}) @filter(uid($uid_second)) {{
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
