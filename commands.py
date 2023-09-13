from typing import Iterable
from datetime import date


from sqlalchemy import select
from sqlalchemy.orm import Session


from menu import menu
from models import Project, Contract


def show_menu(state: str) -> None:
    '''Отобразить меню'''
    for n, action in menu[state].items():
        print(f'[{n}] {action}')
    

def action(state: str) -> int:
    '''Выбрать действие'''
    show_menu(state)
    act = int(input())
    return act


def is_active_contract_exist(session: Session) -> bool:
    '''Проверка существования активного контракта'''
    stmt = select(Contract).where(Contract.status == 'Активен')
    active_contract = session.execute(stmt).fetchall()
    if active_contract:
        return True
    elif not active_contract:
        return False
    

def create_project(session: Session) -> Project:
    '''Создать проект'''
    if is_active_contract_exist(session):
        title = str(input('Введите название проекта:'))
        project = Project(
            title=title,
        )
        session.add(project)
        session.commit()
        print(f'Проект {title} создан!')
        
        return project
    else:
        print('Сначала подтвердите договор!')


def create_contract(session: Session) -> Contract:
    '''Создать договор'''
    title = str(input('Введите название договора:'))
    contract = Contract(
        title=title,
    )
    session.add(contract)
    session.commit()
    print(f'Договор {title} создан!')

    return contract


def fetch_contract(session: Session, id: int) -> Contract | None:
    '''Извлечь договор'''
    stmt = select(Contract).where(Contract.id == id)
    contract: Contract | None = session.execute(stmt).scalar_one_or_none()
    if contract:
        return contract


def fetch_project(session: Session, id: int) -> Project | None:
    '''Извлечь проект'''
    stmt = select(Project).where(Project.id == id)
    project: Project | None = session.execute(stmt).scalar_one_or_none()
    if project:
        return project


def fetch_all_contracts(session: Session):
    '''Извлечь все договоры'''
    contracts: Iterable[Contract] = session.scalars(select(Contract))
    for contract in contracts:
        print(f'ID:{contract.id} ~{contract.title}~')


def fetch_all_projects(session: Session):
    '''Извлечь все проекты'''
    projects: Iterable[Project] = session.scalars(select(Project))
    for project in projects:
        print(f'ID:{project.id} ~{project.title}~')


def fetch_all_entities(session: Session):
    '''Извлечь все сущности'''
    print('----------------')
    print('СПИСОК ПРОЕКТОВ')
    print('----------------')
    fetch_all_projects(session)
    print('----------------')
    print('СПИСОК ДОГОВОРОВ')
    print('----------------')
    fetch_all_contracts(session)
    print('----------------')


def fetch_active_contract_in_project(session: Session, project_id: int) -> Contract | None:
    '''Извлечь активный договор в проекте'''
    stmt = select(Contract).where(Contract.project_id == project_id, Contract.status == 'Активен')
    contract: Contract | None = session.execute(stmt).scalar_one_or_none()
    return contract


def confirm_contract(session: Session, id: int = None) -> None:
    '''Подтвердить договор'''
    id = int(input('Введите ID договора для его подтверждения:'))
    contract = fetch_contract(session, id)
    if not contract.signed and contract.status != 'Завершён':
        contract.status = 'Активен'
        contract.signed = date.today()
        session.commit()
        print(f'Договор *{contract.id} {contract.title}* подтверждён!')
    else:
        print(f'Договор *{contract.id} {contract.title}* уже подтверждён или завершён!')
    

def finalize_contract(session: Session, id: int = None):
    '''Завершить договор'''
    id = int(input('Введите ID договора для его завершения:'))
    contract = fetch_contract(session, id)
    if contract.status != 'Завершён':
        contract.status = 'Завершён'
        session.commit()
        print(f'Договор *{contract.id} {contract.title}* завершён!')
    else:
        print(f'Договор *{contract.id} {contract.title}* уже завершён!')


def add_contract_to_project(session: Session) -> None:
    '''Добавить договор в проект'''
    fetch_all_contracts(session)
    contract_id = int(input('Введите ID договора для добавления его в проект:'))
    contract = fetch_contract(session, contract_id)
    if contract.status == 'Активен' and contract.project_id is None:
        fetch_all_projects(session)
        project_id = int(input('Введите ID проекта, в который хотите добавить договор:'))
        project = fetch_project(session, project_id)
        is_active_contract_in_project = fetch_active_contract_in_project(session, project.id)
        
        if is_active_contract_in_project is None:
            contract.project_id = project.id
            session.commit()
            print(f'Договор *{contract.id} {contract.title}* добавлен в проект *{project.id} {project.title}*!')
        else:
            print(f'В проекте *{project.id} {project.title}* уже есть активный договор!')

    else:
        print(f'Договор *{contract.id} {contract.title}* не активен или имеет проект!')


def finalize_contract_from_project(session: Session) -> None:
    fetch_all_projects(session)
    project_id = int(input('Введите ID проекта, в котором хотите завершить договор:'))
    contract = fetch_active_contract_in_project(session, project_id)
    project = fetch_project(session, project_id)
    
    if contract is None:
        print(f'В проекте *{project.id} {project.title}* нет активного договора!')
    else:
        confirmation = str(input(f'В проекте *{project.id} {project.title}* активный договор — *{contract.id} {contract.title}*.\nВведите "y" для его завершения!'))
        if confirmation == 'y':
            finalize_contract(session, contract.id)
    