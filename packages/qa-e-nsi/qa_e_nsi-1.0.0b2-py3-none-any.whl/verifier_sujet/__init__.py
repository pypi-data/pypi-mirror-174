#!/usr/bin/python

# Copyright (C) 2022 Vincent-Xavier Jumel - All Rights Reversed
# You may use, distribute and modify this code under the
# terms of the GNU GPL-3 license.
#
# You should have received a copy of the GNU GPL-3 license with
# this file. If not, please write to: , or visit :


import argparse
import builtins
import hashlib
import io
import logging
import os
import re
import sys


def lire_fichier(fichier):
    """Lit un fichier, en ne gardant que le code console.

    Args:
        fichier (str): le chemin du fichier à lire

    Returns:
        str: le code source extrait du fichier
    """
    if os.path.splitext(fichier)[-1] == ".md":
        try:
            with open(fichier) as f:
                code_source = ""
                for ligne in f.readlines():
                    if re.match("^(\t| {4})?(<!-- )?(\.\.\.|>>>) ", ligne):
                        code_source = code_source + ligne
            code_source = re.sub("(\t| {4})?(\.\.\.|>>>) ", "", code_source)
            code_source = re.sub("(\t| {4})<!-- ", "", code_source)
            code_source = re.sub("-->", "", code_source)
        except FileNotFoundError as err:
            logging.info(f"{fichier} KO ({err})")
            return ""
    else:
        try:
            with open(fichier) as f:
                code_source = f.read()
        except FileNotFoundError as err:
            logging.info(f"{fichier} KO ({err})")
            return ""
    return code_source


def tester_code(exercice, fichier):
    """Teste le code source passé en argument

    Args:
        exercice (str): chemin du répertoire où est le code source
        fichier (str): fichier du code source
        code_source (str): code source à tester

    Returns:
        bool: un statut succès ou échec des tests
    """

    code_source = lire_fichier(os.path.join(exercice, fichier))

    try:
        exec(code_source, globals())
    except (
        AssertionError,
        IndentationError,
        TypeError,
        SyntaxError,
        ModuleNotFoundError,
        NameError,
        Exception,
    ) as err:
        logging.info(f"'{exercice}/{fichier}' KO ({type(err)} : {err})")
        logging.debug(
            f"""Le code exécuté est \n{code_source}
            """
        )
        return False

    if args.quiet is True:
        logging.info(f"'{exercice}/{fichier}' OK")
    return True


def tester_corrige(repertoire, exercice):
    """Teste le corrigé

    Args:
        repertoire (str): chemin vers le répertoire de travail
        exercice (str): nom de l'exercice

    Returns:
        bool: Échec ou succès
    """
    try:
        chemin_clef = os.path.join(repertoire, exercice, "clef.txt")
        with open(chemin_clef) as f_clef:
            clef = f_clef.read()
            repertoire_clef = hashlib.md5(f"e-nsi+{clef}".encode()).hexdigest()
        repertoire_corr = os.path.join(exercice, repertoire_clef)
    except FileNotFoundError:
        repertoire_corr = exercice
    globals()["__builtins__"] = builtins
    return tester_code(f"{repertoire}/{repertoire_corr}", "exo_corr.py")


def tester_sujet(repertoire, exercice):
    """Teste le sujet

    Args:
        repertoire (str): chemin vers le répertoire de travail
        exercice (str): nom de l'exercice

    Returns:
        bool: Échec ou succès
    """

    return tester_code(os.path.join(repertoire, exercice), "sujet.md")


def tester_test(repertoire, exercice):
    """Teste les tests

    Args:
        repertoire (str): chemin vers le répertoire de travail
        exercice (str): nom de l'exercice

    Returns:
        bool: Échec ou succès
    """

    return tester_code(os.path.join(repertoire, exercice), "exo_test.py")


def tester_tout(repertoire):
    """Teste une arborescence mkdocs complète

    Args:
        repertoire (str): un répertoire contenant un site mkdocs

    Returns:
        bool: Échec ou succès
    """
    statut = []
    for niveau in [_ for _ in os.listdir(repertoire) if "N" in _]:
        for exercice_name in [
            _ for _ in os.listdir(os.path.join(repertoire, niveau)) if "." not in _
        ]:
            if "." not in exercice_name[0] and exercice_name not in args.exclude:
                exercice = os.path.join(niveau, exercice_name)
                statut.append(tester_exercice(repertoire, exercice))
    return all(statut)


def tester_niveau(repertoire):
    """Teste un niveau complet

    Args:
        repertoire (str): un répertoire N* dans un site mkdocs

    Returns:
        bool: Échec ou succès
    """
    statut = []
    for exercice_name in [_ for _ in os.listdir(repertoire) if "." not in _]:
        if "." not in exercice_name[0] and exercice_name not in args.exclude:
            statut.append(tester_exercice(repertoire, exercice_name))
    return all(statut)


def tester_exercice(repertoire, exercice):
    """Tester un exercice

    Args:
        repertoire (str): chemin vers le répertoire de travail
        exercice (str): nom de l'exercice

    Returns:
        bool: Échec ou succès
    """
    statut = []
    statut.append(tester_corrige(repertoire, exercice))
    if args.s is True:
        statut.append(tester_sujet(repertoire, exercice))
    if args.t is True:
        statut.append(tester_test(repertoire, exercice))
    return all(statut)


def tester_presence_niveau(liste_fichier):
    """Tester si une arborescence contient des niveaux

    Args:
        liste_fichier (list): une liste de chemins

    Returns:
        bool: indique si la liste contient bien N0, ..., N4
    """
    return any(
        [os.path.split(elt)[-1] in {f"N{i}" for i in range(5)} for elt in liste_fichier]
    )


def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", default="info")
    parser.add_argument(
        "-x",
        "--exclude",
        help="Fichier à exclure",
        action="append",
        default=[],
        type=str,
    )
    parser.add_argument(
        "--stop_on_first_error",
        help="S'arrête à la première erreur",
        action="store_true",
    )
    parser.add_argument(
        "-q", "--quiet", help="Supprime les sorties OK", action="store_false"
    )

    group = parser.add_argument_group()
    group.add_argument("-s", help="Ne teste que le sujet", action="store_true")
    group.add_argument("-t", help="Ne teste que les tests", action="store_true")

    parser.add_argument(
        "repertoire",
        help="""
        Le répertoire sur lequel agir. Celui-ci peut-être
        un site mkdocs complet ('e-nsi/devel/' ou ('e-nsi/devel/docs')) ;
        un niveau ('e-nsi/devel/docs/N1') ;
        un exercice ('e-nsi/devel/N3/somme_3')
                        """,
    )
    args = parser.parse_args()

    text_trap = io.StringIO()
    sys.stdout = text_trap

    numeric_level = getattr(logging, args.log.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {args.log}")
    logging.basicConfig(level=numeric_level)

    if "docs" in os.listdir(args.repertoire):
        repertoire = os.path.join(args.repertoire, "docs")
        tester_tout(repertoire)
    elif tester_presence_niveau(os.listdir(args.repertoire)):
        repertoire = args.repertoire
        tester_tout(repertoire)
    elif tester_presence_niveau(os.listdir(os.path.join(args.repertoire, os.pardir))):
        repertoire = args.repertoire
        tester_niveau(repertoire)
    elif tester_presence_niveau(
        os.listdir(os.path.join(args.repertoire, os.pardir, os.pardir))
    ):
        exercice = args.repertoire
        repertoire = os.curdir
        tester_exercice(repertoire, exercice)
    else:
        logging.error("Le répertoire indiqué ne semble pas avoir la structure voulue")
        exit(SystemExit())
