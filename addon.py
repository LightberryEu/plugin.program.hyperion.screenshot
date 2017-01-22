import xbmc
import os
import sys
import xbmcaddon
import xbmcgui
import time
import subprocess
import urllib2

addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
addon_dir = xbmc.translatePath( addon.getAddonInfo('path') )
sys.path.append(os.path.join( addon_dir, 'resources', 'lib' ) )
import AddonGithubUpdater

try:
    updater=AddonGithubUpdater.AddonGithubUpdater(addon_dir, "LightberryEu","plugin.program.hyperion.screenshot")
    if updater.isUpdateAvailable():
        if xbmcgui.Dialog().yesno(addonname, "Plugin update is available. Do you want to install new version?"):
            updater.installUpdate()
            xbmcgui.Dialog().ok(addonname, "Update installed. Please restart plugin")
            sys.exit()
except Exception, e:
    xbmcgui.Dialog().ok(addonname, "Failed to check the update...")

line1 = "Welcome!"
line2 = "We take a screenshot now :) Hyperion will be killed in order to enable access to the grabber."

xbmcgui.Dialog().ok(addonname, line1, line2)


try:
    lsusb_output = subprocess.check_output('lsusb')
    grabber=""
    if "1b71:3002" in lsusb_output:
        grabber = "utv007"
    elif "05e1:0408" in lsusb_output:
        grabber = "stk1160"

    if grabber != "":
        if "video0" in subprocess.check_output(['ls','/dev']):
            xbmcgui.Dialog().ok(addonname, "Compatible video grabber has been detected")
        else:
            xbmcgui.Dialog().ok(addonname, "Video grabber has been detected but video0 does not exist. Please install drivers or use different disto")
    else:
        xbmcgui.Dialog().ok(addonname, "We have not detected the grabber. Plugin will exit...")
        sys.exit()

    options = ["PAL", "NTSC"]
    selected_index = xbmcgui.Dialog().select("Select grabber standard:", options)
    # generating screenshot
    if "hyperiond.sh" in subprocess.check_output("ps"):
        subprocess.call(["killall", "hyperiond"])
    os.chdir("/storage")
    if grabber == "utv007":
        xbmcgui.Dialog().ok(addonname,subprocess.check_output(["/storage/hyperion/bin/hyperion-v4l2.sh", "--video-standard", options[selected_index], "--screenshot"]))
    else:
        xbmcgui.Dialog().ok(addonname,subprocess.check_output(["/storage/hyperion/bin/hyperion-v4l2.sh", "--video-standard", options[selected_index], "--width", "240", "--height", "192", "--screenshot"]))
    okno = xbmcgui.WindowDialog(xbmcgui.getCurrentWindowId())
    obrazek = xbmcgui.ControlImage(0,0,1280,720,"/storage/screenshot.png")
    okno.addControl(obrazek)
    okno.show()
    obrazek.setVisible(True)
    time.sleep(5)
    okno.close()
 
except Exception, e:
     xbmcgui.Dialog().ok(addonname, repr(e),"Please report an error at plugin github issue list")


