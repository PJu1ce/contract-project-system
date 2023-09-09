from typing import Iterable

from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import Session, joinedload, selectinload

import config
from models import Base, Project, Contract
from datetime import date


engine = create_engine(url=config.SQLALCHEMY_URL,
                       echo=config.SQLALCHEMY_ECHO,)


def create_project(session: Session, title: str) -> Project:
    project = Project(
        title=title,
    )
    session.add(project)

    session.commit()

    return project


def create_contract(session: Session, title: str) -> Contract:
    contract = Contract(
        title=title,
    )
    session.add(contract)

    session.commit()

    return contract


def fetch_contract(session: Session, id: int) -> Contract | None:
    stmt = select(Contract).where(Contract.id == id)
    contract: Contract | None = session.execute(stmt).scalar_one_or_none()
    return contract


def fetch_all_contracts(session: Session):
    contracts: Iterable[Contract] = session.scalars(select(Contract))
    for contract in contracts:
        print(f'[{contract.id}] {contract.title}')


def fetch_all_projects(session: Session):
    projects: Iterable[Project] = session.scalars(select(Project))
    for project in projects:
        print(f'[{project.id}] {project.title}')


def confirm_contract(session: Session, id: int) -> None:
    contract = session.query(Contract).filter_by(id=id).scalar()
    contract.status = 'Активен'
    if not contract.signed:
        contract.signed = date.today()
    session.commit()


def finalize_contract(session: Session, id: int) -> None:
    contract = session.query(Contract).filter_by(id=id).scalar()
    contract.status = 'Завершён'
    session.commit()


# def add_contract_to_project(session: Session) -> None:
#     fetch_all_projects(session)



def main():
    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        
        while True:
            try:
                pass
            except:
                pass

        
if __name__ == '__main__':
    main()