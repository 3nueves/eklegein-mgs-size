"""user schema"""

class Schema:
    """user schema"""

    query_user_groups ="""query userQuery($uid: string){
        groups(func: uid($uid)){
            User.name
    		groups{
				uid
                Group.name
                Group.mode
                Group.users{
                    uid
                    User.name
                    User.surname
                    Useer.email
                }
            }
          }
        }
    """

    def query_user_one(self, archetype: str, score:str) -> str:
        """Busca usuarios"""

        query = f"""query userQuery($uid:string){{
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
                        ~{archetype}(orderdesc: {score}, first:10) @filter(NOT eq(join_to_team, "Blocked") and NOT eq(join_to_team, "OnHold")) {{
                            uid
                            User.name
                            User.email
                            {score}
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

    def query_user_country_sector(self, archetype: str, score:str) -> str:
        """Busca usuarios nacionalidades y sector"""

        query = f"""query userQuery($uid:string, $country:string, $sector:string){{
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
                    Group.name
                    Group.users{{
                        uid
                        User.email
                    }}
                }}
                {archetype}{{
                    Archetype.name
                    ~relations{{
                        Archetype.name
                        ~{archetype}(orderdesc: {score}, first:10) @filter(eq(country, $country) and eq(sector, $sector) and NOT eq(join_to_team, "Blocked") and NOT eq(join_to_team, "OnHold")) {{
                            uid
                            User.name
                            User.email
                            {score}
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

    query_mails = """
        query get_user($email: string) {
            user(func: eq($email, User.email)) {
                uid
                User.name
                User.surname
                User.email
                secret
            }
        }
        """

    query_mail = """query userQuery($email: string){
            user(func: eq($email, User.email)){
            uid
            User.name
            User.surname
            User.response
            tags
            User.email
            User.disabled
            date
            secret
            country
            sector
            score_hard
            score_medium
            score_soft
            join_to_team
            chats{
                uid
                Chat_users
                Chat_name
                Chat_messages{
                    uid
                    Message_content
                }
            }
            groups{
                uid
			    Group.name
                Group.users{
				    User.name
                }
            }
            archetype_hard{
                Archetype.name
                ~relations{
                    Archetype.name
                    ~archetype_hard(orderdesc: score_hard, first:1){
                        uid
                        User.name
                        score_hard
                        sector
                        country
                    }
                }
            }
            archetype_medium{
                Archetype.name
                ~relations{
                        Archetype.name
                        ~archetype_medium(orderdesc: score_medium, first:1){
                            uid
                            User.name
                            score_medium
                            sector
                            country
                        }
                    }
                }
            archetype_soft{
                Archetype.name
                ~relations{
                    Archetype.name
                    ~archetype_soft(orderdesc: score_soft, first:1){
                        User.name
                        uid
                        score_soft
                        sector
                        country
                    }
                }
            }
        }
    }"""

    query_user = """query userQuery($email: string){
            user(func: eq($email, User.email)){
            uid
            User.name
            User.surname
            tags
            User.email
            date
            country
            sector
            score_hard
            score_medium
            score_soft
            archetype_hard{
                Archetype.name
                ~relations{
                    Archetype.name
                    ~archetype_hard(orderdesc: score_hard, first:1){
                        uid
                        User.name
                        score_hard
                        sector
                        country
                    }
                }
            }
            archetype_medium{
                Archetype.name
                ~relations{
                        Archetype.name
                        ~archetype_medium(orderdesc: score_medium, first:1){
                            uid
                            User.name
                            score_medium
                            sector
                            country
                        }
                    }
                }
            archetype_soft{
                Archetype.name
                ~relations{
                    Archetype.name
                    ~archetype_soft(orderdesc: score_soft, first:1){
                        User.name
                        uid
                        score_soft
                        sector
                        country
                    }
                }
            }
        }
    }
    """
    query_users_relations = """query userQuery($uid: string){
            user(func: uid($uid)){
            uid
            User.name
            User.surname
            User.response
            tags
            User.email
            date
            country
            sector
            score_hard
            score_medium
            score_soft
            archetype_hard{
                uid
                Archetype.name
                ~relations{
                    Archetype.name
                    ~archetype_hard(orderdesc: score_hard, first:1){
                        uid
                        User.name
                        score_hard
                        sector
                        country
                    }
                }
            }
            archetype_medium{
                uid
                Archetype.name
                ~relations{
                        Archetype.name
                        ~archetype_medium(orderdesc: score_medium, first:1){
                            uid
                            User.name
                            score_medium
                            sector
                            country
                        }
                    }
                }
            archetype_soft{
                uid
                Archetype.name
                ~relations{
                    Archetype.name
                    ~archetype_soft(orderdesc: score_soft, first:1){
                        User.name
                        uid
                        score_soft
                        sector
                        country
                    }
                }
            }
        }
    }
    """

    query_users_archetypes_uid = """query userQuery($uid: string){
            user(func: uid($uid)){
            uid
            User.name
            User.surname
            User.response
            tags
            User.email
            date
            country
            sector
            score_hard
            score_medium
            score_soft
            archetype_hard{
                uid
                Archetype.name
            }
            archetype_medium{
                uid
                Archetype.name
                }
            archetype_soft{
                uid
                Archetype.name
            }
        }
    }
    """

    query_user_arch_all = """query userQuery($user: string){
	    user(func: eq(User.name, $user)){
            User.name
            User.surname
            country
            sector
            uid
            archetype_hard{
			    Archetype.name
            }
            archetype_medium{
			    Archetype.name
            }
            archetype_soft{
			    Archetype.name
            }
        }
    }"""

    query_users = """{
	    users(func: has(User.name), first:1){
            User.name
            User.surname
            uid
            User.email
            country
            sector
        }
    }"""

    query_join_to_team = """
        {
            user(func: has(User.email)) {
                uid
                User.name
                User.email
                country
                sector
                join_to_team
                discarded_groups
                groups{
                    uid
                }
            }
        }
        """
    query_group ="""query groupQuery($uid: string){
            group(func: uid($uid)){
            Group.name
            Group.mode
            uid
            date
            Group.chat{
                uid
            }
            Group.users{
                User.name
                User.surname
                User.email
                uid
                }
            }
        }
        """

    query_group_all ="""query groupQuery($uid: string){
        group(func: uid($uid)){
        Group.name
        date
        Group.users{
            User.name
            uid
            archetype_hard{
                Archetype.name
                ~relations{
                    Archetype.name
                    ~archetype_hard(orderdesc: score_hard, first:2){
                        uid
                        User.name
                        score_hard
                        sector
                        country
                    }
                }
            }
            archetype_medium{
                Archetype.name
                ~relations{
                    Archetype.name
                    ~archetype_medium(orderdesc: score_medium, first:2){
                            uid
                            User.name
                            score_medium
                            sector
                            country
                    }
                }
            }
            archetype_soft{
            Archetype.name
                ~relations{
                    Archetype.name
                    ~archetype_medium(orderdesc: score_medium, first:2){
                        uid
                        User.name
                        score_medium
                        sector
                        country
                    }
                }
            }
        }
        }
        }
        """

    query_all_groups ="""
    {
        group(func: has(Group.name)){
        uid
        Group.name
        date
        Group.status
        Group.chat
        Group.date_add_users{
            uid
            date
        }
        Group.users{
            User.name
            join_to_team
            User.email
            country
            sector
            uid
            groups{
                uid
            }
            # archetype_hard{
            #     Archetype.name
            # }
            # archetype_medium{
            #     Archetype.name
            # }
            # archetype_soft{
            # 	Archetype.name
            # }
        }
      }
    } 
    """
