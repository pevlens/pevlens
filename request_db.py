from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.sqltypes import Boolean
from creare_model import User, Base
from config import PG_USER, host, PG_PASS
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta




class DBComands():


    def __init__(self, user = PG_USER, passwd = PG_PASS, host = host) -> None:
        self.engine = create_engine(f"postgresql://{PG_USER}:{PG_PASS}@{host}:5432/test")
        Base.metadata.bind = self.engine
        DBSession = sessionmaker(bind=self.engine)
        self.session = DBSession()
         

    
    def add_new_user (self, chat_id : int , username : str, fullname: str, reveral = None ) -> User:

        
        try:
            user = User(chat_id = chat_id, username= username, full_name=fullname, reveral = reveral)
            self.session.add(user) 
            self.session.commit()
            #self.session.close()
            if self.session.query(User).filter_by(chat_id = reveral).first():
                self.update_balance_user(reveral, 100)
            return f"Пользователь {username} успешно добавлен"
        except IntegrityError:
            self.session.close()
            return f"Пользователь {username} уже есть в базе"

        except Exception:
             self.session.rollback()
        finally:
            self.session.close()
        
       


    
    def  update_balance_user (self, chat_id: int, add_balance: int ) -> int:
        
        update_balance_user =self.session.query(User).filter_by(chat_id = chat_id).one()
        update_balance_user.balance +=  add_balance
        self.session.add(update_balance_user) 
        self.session.commit()
        self.session.close()
        return f'Пользрвателю добавленно {add_balance}'

    
    def  view_balance_user (self, chat_id: int ) -> int:
        
        update_balance_user = self.session.query(User).filter_by(chat_id = chat_id).first()
        return f'Текущий баланс пользователя {update_balance_user.balance}'

    
    def  count_referal_user (self, chat_id: int ) -> int:
        
        count_referal_user = self.session.query(User).filter_by(reveral = chat_id).count()
        return f'У вас {count_referal_user} приглашенных поьзователей'

    
    def time_update(self, chat_id) -> Boolean:
        time_update_balance_last = self.session.query(User).filter_by(chat_id = chat_id).first()
        time_now= datetime.now()
        delta = time_now - time_update_balance_last.time_update
        return str(delta) ,delta > timedelta(seconds=10)

    
    def  set_moey_user (self, chat_id: int, sum: int) -> int:
        
        set_balance_user = self.session.query(User).filter_by(chat_id = chat_id).one()
        if sum <=  set_balance_user.balance:
            set_balance_user.balance -=  sum
            self.session.add(set_balance_user) 
            self.session.commit()
            self.session.refresh(set_balance_user)
            self.session.expunge(set_balance_user)
            
            self.session.close()
            return f'выведено {sum} текущий баланс {set_balance_user.balance}'
        else:
            return f"вы ввели не верную сумму"
        #return f'Текущий баланс пользователя {update_balance_user.balance}'

if __name__ == '__main__':
    
    obj = DBComands()
    #print(obj.add_new_user(543211, "ujin", "qwerty_pouj", 1234))
    #print(obj.view_balance_user(1234))
    #print(obj.count_referal_user(1234))
    #print(obj.time_update(581018614))
   
    #print(obj.update_balance_user(581018614, 100))
    
   