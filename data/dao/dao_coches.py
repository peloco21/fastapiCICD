from data.modelo.coche import Coche
from fastapi import HTTPException

class DaoCoches:
    def get_all(self, db) -> list[Coche]:
        cursor = db.cursor()
        
        cursor.execute("SELECT id, modelo FROM coches")
        
        coches_en_db = cursor.fetchall()
        
        coches: list[Coche] = []
        
        for coche in coches_en_db:
            coche_obj = Coche(coche[0], coche[1])
            coches.append(coche_obj)
        
        cursor.close()
        return coches

    def add(self, db, coche: Coche):
        cursor = db.cursor()
        if coche.modelo:
            cursor.execute("INSERT INTO coches (modelo) VALUES (%s)", (coche.modelo,))
        db.commit()
        cursor.close()

    def delete(self, db, modelo: str):
        cursor = db.cursor()
    
    
        cursor.execute("SELECT * FROM coches WHERE modelo = %s", (modelo,))
        coche = cursor.fetchone()
    
        if not coche:
            raise HTTPException(status_code=404, detail=f"No se encontró el coche con modelo '{modelo}'")
    
   
        cursor.execute("DELETE FROM coches WHERE modelo = %s", (modelo,))
        db.commit()
        cursor.close()


