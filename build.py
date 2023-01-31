#!/bin/env python3
import sys
import os
from subprocess import call
import shutil
from pathlib import Path

projects = [("com.eduke32.EDuke32","x86_64"),
        ("co.uk.pcemulator.PCem","x86_64"),
        ("io.github.Mednafen","x86_64"),
        ("io.github.SameBoy","x86_64"),
        ("net.pcsx2.PCSX2","x86_64"),
        ("org.libretro.RetroArch","x86_64"),
        ("commercial/com.github.wolf4sdl","x86_64"),
        ("commercial/com.rimworldgame.RimWorld","x86_64"),
        ("commercial/org.freegish.Gish","x86_64"),
        ("commercial/org.ioquake.ioq3","x86_64"),
        ("commercial/org.iortcw.iortcwSP","x86_64"),
        ("io.github.m64p","x86_64"),
        ("org.neverball.Neverball","x86_64"),
        ("net.kuribo64.melonDS","x86_64"),
        ("com.retrodev.blastem","x86_64"),
        ("org.DolphinEmu.dolphin-emu","x86_64"),
        ("org.ppsspp.PPSSPP","x86_64"),
        ("io.mgba.mGBA","x86_64"),
        ("org.byuu.bsnes","x86_64"),
        ("net.sourceforge.quakespasm","x86_64"),
        ("io.github.pr-starfighter","x86_64"),
        ("com.github.Sude.lgogdownloader","x86_64"),
        ("com.valvesoftware.Steam.Utility.gamescope","x86_64"),
        ("commercial/com.factorio.factorio","x86_64"),
        ("org.winehq.Wine","x86_64"),
        ("org.mamedev.MAME","x86_64")]

def main():
    repo_path = sys.argv[1]
    filter_name = None
    update_only = False
    if len(sys.argv) > 2:
        val = sys.argv[2]
        if val == 'update_only':
            update_only = True
        else:
            filter_name = val

    home = str(Path.cwd().parent)
    proj_prefix = os.path.join(home, "flatpak")
    results = []

    call(["git", "submodule", "update", "--recursive", "--remote", "--merge"])
    for proj in projects:
        path = proj[0]
        if filter_name:
            if not filter_name in path:
                continue

        arch = proj[1]
        full_path = os.path.join(os.path.expanduser(proj_prefix), path)
        name = path.split("/")[-1]

        stats_dir = os.path.join(home, "build-dir", name, "flatpak-builder")
        build_dir = os.path.join(home, "build-dir", name, "build")

        os.chdir(full_path)

        if os.path.isfile(name+".json"):
            name += ".json"
        else:
            name += ".yml"

        print(name)
        call(["chrt", "-i", "0", "flatpak", "run", "org.flathub.flatpak-external-data-checker", "--commit-only", "--edit-only", name])
        if not update_only:
            ret = call(["chrt", "-i", "0", "flatpak-builder", "--jobs=7", build_dir, name, "--force-clean", "--repo="+repo_path, "--arch="+arch, "--state-dir="+stats_dir])
            #ret = call(["chrt", "-i", "0", "flatpak", "run", "org.flatpak.Builder", build_dir, name, "--force-clean", "--repo="+repo_path, "--arch="+arch, "--state-dir="+stats_dir])
            results.append(name + " -> " + str(ret))

        #shutil.rmtree("build", ignore_errors=True)
        #shutil.rmtree(".flatpak-builder", ignore_errors=True)

    for r in results:
        print(r)

if __name__ == "__main__":
    main()
