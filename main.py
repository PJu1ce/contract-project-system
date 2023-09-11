from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import config
from commands import *
from models import Base

engine = create_engine(url=config.SQLALCHEMY_URL,
                       echo=config.SQLALCHEMY_ECHO,)


def main():
    Base.metadata.create_all(bind=engine)
    state = 'Меню'

    with Session(engine) as session:
        
        while True:
            try:
                match state:
                     
                    case 'Меню':
                        act = action(state)
                        state = menu[state][act]
                    
                    case 'Просмотр проектов и договоров':
                        fetch_all_entities(session)
                        state = 'Меню'

                    case 'Проект':
                        act = action(state)
                        state = menu[state][act]

                    case 'Создать проект':
                        create_project(session)
                        state = 'Меню'

                    case 'Договор':
                        act = action(state)
                        state = menu[state][act]

                    case 'Добавить договор в проект':
                        add_contract_to_project(session)
                        state = 'Меню'

                    case 'Создать договор':
                        create_contract(session)
                        state = 'Меню'

                    case 'Подтвердить договор':
                        fetch_all_contracts(session)
                        confirm_contract(session)
                        state = 'Меню'

                    case 'Завершить договор':
                        fetch_all_contracts(session)
                        finalize_contract(session)
                        state = 'Меню'

                    case 'Завершить договор с выбором проекта':
                        finalize_contract_from_project(session)
                        state = 'Меню'

                    case 'Завершить работу':
                        break
                    
            except:
                pass
                

        
if __name__ == '__main__':
    main()