from teste import Farmacia
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import logging

def get_fralda_data():
    engine = create_engine('sqlite:///fraldario.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        farmacias = session.query(Farmacia).all()
        result = []
        for farmacia in farmacias:
            data_retirada = farmacia.data_retirada.strftime('%Y-%m') if farmacia.data_retirada else 'N/A'
            result.append({
                'farmacia': farmacia.nomeFantasia,
                'quantidade': farmacia.quantidadeTotal,
                'mes': data_retirada,
                'data_retirada': farmacia.data_retirada.strftime('%Y-%m-%d') if farmacia.data_retirada else 'N/A'
            })
        logging.info(f"Dados de fraldas carregados: {result}")
        return result
    except Exception as e:
        logging.error(f"Erro ao carregar dados de fraldas: {e}")
        return []
    finally:
        session.close()
