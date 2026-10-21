from django.db import models

# Create your models here.
class Pays(models.Model):
    nom = models.CharField(max_length=100)
    tva = models.FloatField()
    tarif_electrique = models.FloatField()
    salaire_minimum = models.FloatField()

    def __str__(self):
       return self.nom

class Ville(models.Model):
    nom = models.CharField(max_length=100)
    taxe_immobiliere = models.FloatField()
    prix_m2 = models.FloatField()
    pays = models.ForeignKey(
            Pays, on_delete=models.PROTECT,
    )
    def __str__(self):
        return self.nom

class Machine(models.Model):
    nom = models.CharField(max_length=100)
    prix = models.FloatField()
    duree_de_vie = models.FloatField()
    cout_maintenance = models.FloatField()
    superficie = models.FloatField()
    def __str__(self):
       return self.nom

class QuantiteMachine(models.Model):

    machine = models.ForeignKey(
        Machine, on_delete=models.PROTECT,
    )
    nombre = models.IntegerField()

    def __str__(self):
      return f"{self.nombre} x {self.machine.nom}"

class Lieu(models.Model):

    nom = models.CharField(max_length=100)
    ville = models.ForeignKey(
       Ville, on_delete=models.PROTECT,

    )
    superficie = models.FloatField()
    quantite_machines = models.ManyToManyField(
           QuantiteMachine, blank=True
    )
    consommation_electrique = models.FloatField()

    def __str__(self):
       return self.nom

class Transport(models.Model):

    nombre_palettes = models.IntegerField()
    cout = models.FloatField()
    delai = models.FloatField()
    depart = models.ForeignKey(
           Lieu, on_delete=models.PROTECT, related_name="transports_depart"


    )
    arrivee = models.ForeignKey(
               Lieu, on_delete=models.PROTECT, related_name="transports_arrivee"


    )


    def __str__(self):
       return f"Transport {self.depart.nom} -> {self.arrivee.nom} "

class Operation(models.Model):

    nom = models.CharField(max_length=100)
    operation_suivante = models.ForeignKey(
               "self", on_delete=models.SET_NULL,
                null=True,
                blank=True,
                related_name="operation_precedentes"
    )
    cout = models.FloatField()
    machine = models.ForeignKey(
               Machine, on_delete=models.PROTECT,


    )
    quantite_produits = models.ManyToManyField(
               "QuantiteProduit", blank=True
    )
    heures_de_travail = models.FloatField()
    consommation_electrique = models.FloatField()

    def __str__(self):
       return self.nom


class Produit(models.Model):

    nom = models.CharField(max_length=100)
    prix_de_vente = models.FloatField()
    duree_de_vie = models.FloatField()
    nombre_par_palette = models.IntegerField()

    operations = models.ManyToManyField(Operation, blank=True)


    def __str__(self):
       return self.nom

class PrixProduit(models.Model):

    produit = models.ForeignKey(
            Produit, on_delete=models.PROTECT,

    )
    prix_achat = models.FloatField()

    def __str__(self):
       return f"{self.produit.nom} : {self.prix_achat}€"


class Fournisseur(models.Model):

    nom = models.CharField(max_length=100)

    prix_produits = models.ManyToManyField(
                PrixProduit  , blank=True
    )

    def __str__(self):
       return self.nom


class QuantiteProduit(models.Model):

    produit = models.ForeignKey(
            Produit, on_delete=models.PROTECT,

    )

    nombre = models.IntegerField()



    def __str__(self):
       return f"{self.nombre} x {self.produit.nom}"


class Stock(models.Model):

    quantite_produits = models.ManyToManyField(QuantiteProduit, blank=True)

    palettes_max = models.IntegerField()
    def __str__(self):
       return f"Stock (max : {self.palettes_max} palettes)"

class PointDeVente(models.Model):

    nom = models.CharField(max_length=100)
    lieu =  models.ForeignKey(
        Lieu, on_delete=models.PROTECT,

        )
    heures_de_travail = models.FloatField()
    stock =  models.ForeignKey(
        Stock, on_delete=models.PROTECT,

        )
    def __str__(self):
       return self.nom


class Facture(models.Model):

    quantite_produits = models.ManyToManyField(
                    QuantiteProduit , blank=True
        )

    reduction = models.FloatField()
    point_de_vente = models.ForeignKey(
        PointDeVente, on_delete=models.PROTECT,

        )
    client = models.CharField(max_length=100)

    def __str__(self):
        return f"Facture {self.client} - {self.point_de_vente.nom}"
