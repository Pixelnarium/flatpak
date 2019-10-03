#!/bin/env python3
import sys
import os
from subprocess import call
import shutil

projects = [("com.dosbox.DOSBox","x86_64"),
        ("com.eduke32.EDuke32","x86_64"),
        ("co.uk.pcemulator.PCem","x86_64"),
        ("io.github.Mednafen","x86_64"),
        ("io.github.SameBoy","x86_64"),
        ("net.pcsx2.PCSX2","i386"),
        ("org.libretro.RetroArch","x86_64"),
        ("commercial/com.github.wolf4sdl","x86_64"),
        ("commercial/com.factorio.factorio","x86_64"),
        ("commercial/com.rimworldgame.RimWorld","x86_64"),
        ("commercial/org.freegish.Gish","x86_64"),
        ("commercial/org.ioquake.ioq3","x86_64"),
        ("commercial/org.iortcw.iortcwSP","x86_64"),
        ("io.github.m64p","x86_64"),
        ("org.neverball.Neverball","x86_64"),
        ("net.kuribo64.melonds","x86_64"),
        ("com.retrodev.blastem","x86_64"),
        ("org.byuu.bsnes","x86_64")]


def main():
    repo_path = sys.argv[1]
    proj_prefix = "~/FlatPak/flatpak/"
    results = []

    for proj in projects:
        path = proj[0]
        arch = proj[1]
        full_path = os.path.expanduser(proj_prefix+path)
        name = path.split("/")[-1]

        os.chdir(full_path)

        if os.path.isfile(name+".json"):
            name += ".json"
        else:
            name += ".yml"

        ret = call(["flatpak-builder", "build", name, "--force-clean", "--repo="+repo_path, "--arch="+arch])
        results.append(name + " -> " + str(ret))

        shutil.rmtree("build", ignore_errors=True)
        shutil.rmtree(".flatpak-builder", ignore_errors=True)

    for r in results:
        print(r)

if __name__ == "__main__":
    main()
