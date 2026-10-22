# high_level/tests.py
#from django.test import TestCase

#from .models import Machine


#class MachineModelTests(TestCase):

    #def test_machine_creation(self):
       # self.assertEqual(Machine.objects.count(), 0)
        #Machine.objects.create(nom="cabine_peinture", prix=18_000, duree_de_vie=8.0  , cout_maintenance= 600.0  , superficie= 15.0 )
        #self.assertEqual(Machine.objects.count(), 1)
from django.test import TestCase
from .models import (
    Lieu,
    Machine,
    Pays,
    PointDeVente,
    Produit,
    QuantiteMachine,
    QuantiteProduit,
    Stock,
    Ville,
)


class LieuCostsTests(TestCase):

    def test_calcul_cout_lieu_scenario(self):
        # 1. Pays (tarif_electrique = 0.2 €/kWh)
        pays = Pays.objects.create(
            nom="France",
            tva=20.0,
            tarif_electrique=0.2,
            salaire_minimum=12.0,
        )

        # 2. Ville (prix_m2 = 2000 €/m²)
        ville = Ville.objects.create(
            nom="Labège",
            taxe_immobiliere=0.0,
            prix_m2=2000.0,
            pays=pays,
        )

        # 3. Lieu (50 m², 5000 kWh) -> Coût immo (100 000 €) + Elec (1 000 €)
        lieu = Lieu.objects.create(
            nom="Entrepôt Labège",
            superficie=50.0,
            consommation_electrique=5000.0,
            ville=ville,
        )

        # 4. Machine à 5 000 €
        m_5k = Machine.objects.create(
            nom="Machine 5k",
            prix=5000.0,
            duree_de_vie=5.0,
            cout_maintenance=200.0,
            superficie=5.0,
        )
        qm_5k = QuantiteMachine.objects.create(machine=m_5k, nombre=1)
        lieu.quantite_machines.add(qm_5k)

        # 5. Stock : 2 palettes acier (2 000 €) + 1 palette câbles (3 000 €) = 5 000 €
        p_acier = Produit.objects.create(
            nom="Palette tubes acier",
            prix_de_vente=1000.0,
            duree_de_vie=5.0,
            nombre_par_palette=1,
        )
        p_cables = Produit.objects.create(
            nom="Palette câbles",
            prix_de_vente=3000.0,
            duree_de_vie=5.0,
            nombre_par_palette=1,
        )

        qp_acier = QuantiteProduit.objects.create(produit=p_acier, nombre=2)
        qp_cables = QuantiteProduit.objects.create(produit=p_cables, nombre=1)

        stock = Stock.objects.create(palettes_max=10)
        stock.quantite_produits.add(qp_acier, qp_cables)

        PointDeVente.objects.create(
            nom="PDV Labège",
            lieu=lieu,
            heures_de_travail=35.0,
            stock=stock,
        )

        # 6. Affichage et validation (100 000 + 1 000 + 5 000 + 5 000 = 111 000 €)
        lieu_test = Lieu.objects.first()
        print(f"\n---> Coût affiché : {lieu_test.costs()} €")
        self.assertEqual(lieu_test.costs(), 111000.0)
