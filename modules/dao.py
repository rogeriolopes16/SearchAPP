from modules.models import Cadastro, Obj

SQL_BUSCA_USR_SEARCH = "select DISTINCT upper(owner.displayName) AS NOME, upper(owner.email) EMAIL, (select upper(att.value) from EntryAttributeValue att where att.entry_id = owner.id and att.name = 'userType') as TIPO, \
(select upper(att.value) from EntryAttributeValue att where att.entry_id = owner.id and att.name = 'location') as EMPRESA, (select upper(att.value) from EntryAttributeValue att where att.entry_id = owner.id and att.name = 'managerName') as RESP \
from (ANALYTICS_USER_VIEW owner join EntryAttributeValue EntryAttributeValue on ((EntryAttributeValue.entry_id = owner.id))) WHERE owner.state = 'ACTIVE' and owner.displayName like %s ORDER BY 1"


SQL_BUSCA_USR_SEARCH_RESP = "select DISTINCT upper(owner.displayName) AS NOME, upper(owner.email) EMAIL, (select upper(att.value) from EntryAttributeValue att where att.entry_id = owner.id and att.name = 'userType') as TIPO, \
(select upper(att.value) from EntryAttributeValue att where att.entry_id = owner.id and att.name = 'location') as EMPRESA, (select upper(att.value) from EntryAttributeValue att where att.entry_id = owner.id and att.name = 'managerName') as RESP \
from (ANALYTICS_USER_VIEW owner join EntryAttributeValue EntryAttributeValue on ((EntryAttributeValue.entry_id = owner.id))) WHERE owner.state = 'ACTIVE' and (select att.value from EntryAttributeValue att where att.entry_id = owner.id and att.name = 'managerName') like %s ORDER BY 1"

SQL_BUSCA_OBJ_SEARCH = "SELECT 'RECURSO' TIPO, upper(r.name) DESCRICAO, upper(w.OWNER) FROM Resource r left join RESOURCE_OWNERS_VIEW w on r.name = w.RESOURCE where r.name like %s UNION ALL \
SELECT 'DIREITO' TIPO, CONCAT(upper(e.name), '   -----> (RECURSO: ',upper(r.name),')') DESCRICAO, \
if(w.OWNER is not NULL, upper(w.OWNER), (SELECT upper(wo.OWNER) FROM RESOURCE_OWNERS_VIEW wo where wo.RESOURCE = r.name)) as OWNER \
FROM Entitlement e inner join Resource r on r.id = e.resource_id left join ENTITLEMENTS_OWNERS_VIEW w on w.ENTITLEMENT= e.name where e.name like %s UNION ALL \
SELECT 'PAPEL' TIPO, r.name DESCRICAO, w.OWNER FROM Role r left join ROLES_OWNERS_VIEW w on r.name = w.ROLE where r.name like %s ORDER BY 1 DESC, 2"

SQL_BUSCA_OBJ_SEARCH_RESP = "SELECT 'RECURSO' TIPO, upper(r.name) DESCRICAO, upper(w.OWNER) FROM Resource r left join RESOURCE_OWNERS_VIEW w on r.name = w.RESOURCE where w.OWNER like %s UNION ALL \
SELECT 'DIREITO' TIPO, CONCAT(upper(e.name), '   -----> (RECURSO: ',upper(r.name),')') DESCRICAO, \
if(w.OWNER is not NULL, upper(w.OWNER), (SELECT upper(wo.OWNER) FROM RESOURCE_OWNERS_VIEW wo where wo.RESOURCE = r.name)) as OWNER \
FROM Entitlement e inner join Resource r on r.id = e.resource_id left join ENTITLEMENTS_OWNERS_VIEW w on w.ENTITLEMENT= e.name \
where if(w.OWNER is not NULL, w.OWNER, (SELECT wo.OWNER FROM RESOURCE_OWNERS_VIEW wo where wo.RESOURCE = r.name)) like %s UNION ALL \
SELECT 'PAPEL' TIPO, upper(r.name) DESCRICAO, upper(w.OWNER) FROM Role r left join ROLES_OWNERS_VIEW w on r.name = w.ROLE where w.OWNER like %s ORDER BY 1 DESC, 2"

class SearchDao:
    def __init__(self, db):
        self.__db = db

    def listarSearch(self,search):
        cursor = self.__db.cursor()
        cursor.execute(SQL_BUSCA_USR_SEARCH, ("%" + search + "%",))
        cadastros = traduz_cad(cursor.fetchall())
        self.__db.commit()
        return cadastros

    def listarSearchResp(self,search):
        cursor = self.__db.cursor()
        cursor.execute(SQL_BUSCA_USR_SEARCH_RESP, ("%" + search + "%",))
        cadastros = traduz_cad(cursor.fetchall())
        self.__db.commit()
        return cadastros


    def listarSearchObj(self,search):
        cursor = self.__db.cursor()
        cursor.execute(SQL_BUSCA_OBJ_SEARCH, ("%" + search + "%","%" + search + "%","%" + search + "%"))
        cadastros = traduz_obj(cursor.fetchall())
        self.__db.commit()
        return cadastros

    def listarSearchRespObj(self,search):
        cursor = self.__db.cursor()
        cursor.execute(SQL_BUSCA_OBJ_SEARCH_RESP, ("%" + search + "%","%" + search + "%","%" + search + "%"))
        cadastros = traduz_obj(cursor.fetchall())
        self.__db.commit()
        return cadastros


def traduz_cad(cad):
    def cria_cad_com_tupla(tupla):
       return Cadastro(tupla[0], tupla[1], tupla[2], tupla[3], tupla[4])
    return list(map(cria_cad_com_tupla, cad))

def traduz_obj(cad):
    def cria_cad_com_tupla(tupla):
       return Obj(tupla[0], tupla[1], tupla[2])
    return list(map(cria_cad_com_tupla, cad))