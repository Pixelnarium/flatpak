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

self_host = [("https://github.com/flathub/com.visualstudio.code.git","com.visualstudio.code")]

sh_folder = "selfhost"

def checkout_selfhosted(proj_prefix):
    sh_path = proj_prefix.joinpath(sh_folder)
    os.chdir(proj_prefix)
    shutil.rmtree(sh_folder, ignore_errors=True)

    for selfh in self_host:
        sgit = selfh[0]
        sname = selfh[1]
        call(["git", "clone", "--depth=1", sgit, str(sh_path.joinpath(sname))])
        projects.append((sh_folder+"/"+sname, "x86_64"))
        shutil.copytree(str(proj_prefix.joinpath("shared-modules")), str(sh_path.joinpath(sname, "shared-modules")), dirs_exist_ok=True) 

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

    home = Path.cwd().parent
    proj_prefix = home.joinpath("flatpak")
    
    results = []

    call(["git", "submodule", "update", "--recursive", "--remote", "--merge"])

    checkout_selfhosted(proj_prefix)

    for proj in projects:
        path = proj[0]
        if filter_name:
            if not filter_name in path:
                continue

        arch = proj[1]
        full_path = proj_prefix.joinpath(path)
        name = path.split("/")[-1]

        stats_dir = home.joinpath("build-dir", name, "flatpak-builder")
        build_dir = home.joinpath("build-dir", name, "build")

        os.chdir(full_path)

        if os.path.isfile(name+".json"):
            name += ".json"
        else:
            if os.path.isfile(name+".yml"):
                name += ".yml"
            else:
                name += ".yaml"

        print(name)
        call(["chrt", "-i", "0", "flatpak", "run", "org.flathub.flatpak-external-data-checker", "--commit-only", "--edit-only", name])
        if not update_only:
            ret = call(["chrt", "-i", "0", "flatpak-builder", "--jobs=4", str(build_dir), name, "--force-clean", "--repo="+repo_path, "--arch="+arch, "--state-dir="+str(stats_dir)])
            results.append(name + " -> " + str(ret))

        #shutil.rmtree("build", ignore_errors=True)
        #shutil.rmtree(".flatpak-builder", ignore_errors=True)

    for r in results:
        print(r)

if __name__ == "__main__":
    main()
