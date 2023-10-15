import base64
import pandas as pd
import io


class StatemantTransform:
    def __init__(self, contents):
        self.contents = contents

    def _decode_contents(self):
        content_type, content_string = self.contents.split(',')
        decoded = base64.b64decode(content_string)
        return pd.read_csv(io.StringIO(decoded.decode('utf-8')))

    def transform_wise(self):
        df_file_uploaded = self._decode_contents()

        df_file_uploaded = df_file_uploaded.dropna(axis=1, how='all')
        df_file_uploaded = df_file_uploaded[df_file_uploaded['Situação'] != 'Cancelado']

        receitas_file_uploaded = df_file_uploaded[df_file_uploaded['Direção'] == 'IN']
        despesas_file_uploaded = df_file_uploaded[df_file_uploaded['Direção'] == 'OUT']

        receitas_transformed = pd.DataFrame({
            'Valor': receitas_file_uploaded['Valor de destino (tarifas inclusas)'],
            'Efetuado': 1,
            'Fixo': 0,
            'Data': pd.to_datetime(receitas_file_uploaded['Concluída em']),
            'Categoria': 'Outros',
            'Descrição': receitas_file_uploaded['Nome de origem']
        })

        despesas_transformed = pd.DataFrame({
            'Valor': despesas_file_uploaded['Valor de origem (tarifas inclusas)'],
            'Efetuado': 1,
            'Fixo': 0,
            'Data': despesas_file_uploaded['Concluída em'],
            'Categoria': 'Outros',
            'Descrição': despesas_file_uploaded['Nome do beneficiário']
        })

        return receitas_transformed, despesas_transformed
    
    def transform_cgd(self):
        df_file_uploaded = self._decode_contents()

        df_file_uploaded = df_file_uploaded.dropna(axis=1, how='all') ## drop columns with all NaN values

        receitas_file_uploaded = df_file_uploaded[df_file_uploaded['Tipo'] == 'Entrada']
        despesas_file_uploaded = df_file_uploaded[df_file_uploaded['Tipo'] == 'Saída']

        receitas_transformed = pd.DataFrame({
            'Valor': receitas_file_uploaded['Valor'],
            'Moeda': receitas_file_uploaded['Moeda de destino'], ## 'Moeda de origem' or 'Moeda de destino
            'Efetuado': 1,
            'Fixo': 0,
            'Data': pd.to_datetime(receitas_file_uploaded['Concluída em']),
            'Categoria': 'Outros',
            'Descrição': receitas_file_uploaded['Nome de origem']
        })

        despesas_transformed = pd.DataFrame({
            'Valor': despesas_file_uploaded['Valor'],
            'Moeda': despesas_file_uploaded['Moeda de destino'],
            'Efetuado': 1,
            'Fixo': 0,
            'Data': despesas_file_uploaded['Concluída em'],
            'Categoria': 'Outros',
            'Descrição': despesas_file_uploaded['Nome do beneficiário']
        })

        # return receitas_transformed, despesas_transformed
        return None, None
    
    def transform_nubank(self): ...
    def transform_inter(self): ...

