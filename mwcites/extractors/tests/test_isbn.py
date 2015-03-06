import pprint
from nose.tools import eq_

from .. import isbn
from ...identifier import Identifier

INPUT_TEXT = """
    | publisher=Academic Press | isbn=0124366031
    | isbn=3540206310
    | accessdate=2008-02-05 | isbn=0-618-34342-3
    | isbn=978-0-140-27666-4
    | isbn = 0-13-054091-9
    | isbn=0195305736 }}&lt;/ref&gt; schlug [[Irving Langmuir]] 1919 vor, dass das Elektronen in einem Atom verbunden oder verklumpt seien. Elektronengruppen beset
    | ISBN=978-3-7046-5112-9
    * Peter L. Bergen: ''Heiliger Krieg, Inc.: Osama bin Ladens Terrornetz''. Siedler, Berlin 2001, ISBN 3-88680-752-5.
    * Marwan Abou-Taam, Ruth Bigalke (Hgg) ''Die Reden des Osama bin Laden''. Diederichs, München 2006, ISBN 3-72052-773-5. (Reden und Ansprachen des b.L. im Original - ''Rezensionen: '' [http://www.sicherheit-heute.de/index.php?cccpage=readpolitik&amp;set_z_artikel=221 ]und [http://www.fr-online.de/in_und_ausland/kultur_und_medien/buecher/?em_cnt=868715&amp;sid=f55727] Frankf. Rundschau 26. April 2006)
    * Michael Pekler, Andreas Ungerböck: ''Ang Lee und seine Filme''. Schüren, Marburg 2009, ISBN 978-3-89472-665-2.
    &lt;ref name=&quot;flos1&quot;&gt;{{Literatur | Autor = René Flosdorff, Günther Hilgarth | Titel = Elektrische Energieverteilung | Verlag = Teubner | Auflage = 8. | Jahr = 2003 | Kapitel = Kapitel 1.2.2.4 | ISBN = 3-519-26424-2 }}&lt;/ref&gt;
    Bei einer [[Sprungtemperatur]] von 1,2&amp;nbsp;K wird reines Aluminium [[Supraleiter|supraleitend]].&lt;ref&gt;{{Literatur | Autor = Ilschner | first = Bernhard | Titel = Werkstoffwissenschaften und Fertigungstechnik Eigenschaften, Vorgänge, Technologien | Verlag = Springer | Ort = Berlin | Jahr = 2010 | ISBN = 978-3-642-01734-6 | Seiten = 277}}&lt;/ref&gt;
    * {{Literatur | Autor=Michael J. Padilla, Ioannis Miaoulis, Martha Cyr | Jahr = 2002 | Titel = Prentice Hall Science Explorer: Chemical Building Blocks | Verlag = Prentice-Hall, Inc. | Ort = Upper Saddle River, New Jersey USA | ISBN = 0-13-054091-9 | |Originalsprache=en}}
    """


EXPECTED = [
    Identifier('isbn', '0124366031'),
    Identifier('isbn', '3540206310'),
    Identifier('isbn', '0618343423'),
    Identifier('isbn', '9780140276664'),
    Identifier('isbn', '0130540919'),
    Identifier('isbn', '0195305736'),
    Identifier('isbn', '9783704651129'),
    Identifier('isbn', '3886807525'),
    Identifier('isbn', '3720527735'),
    Identifier('isbn', '9783894726652'),
    Identifier('isbn', '3519264242'),
    Identifier('isbn', '9783642017346'),
    Identifier('isbn', '0130540919'),
]

def test_extract():
    ids = list(isbn.extract(INPUT_TEXT))
    pprint.pprint(ids)
    pprint.pprint(EXPECTED)
    eq_(ids, EXPECTED)
