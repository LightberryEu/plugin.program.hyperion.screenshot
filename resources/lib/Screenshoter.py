import subprocess, os

class Screenshoter:
    def __init__(self):
        self.isOSMC = "osmc" in open("/proc/version").read()
        pass

    def takeScreenshot(self, path, videoStandard):
        os.chdir(path)

        lsusbOutput = subprocess.check_output('lsusb')
        grabber = ""
        if "1b71:3002" in lsusbOutput:
            grabber = "utv007"
        elif "05e1:0408" in lsusbOutput:
            grabber = "stk1160"

        if grabber != "":
            if "video0" not in subprocess.check_output(['ls', '/dev']):
                raise Exception("Video grabber has been detected but video0 does not exist. Please install drivers or use different disto")
        else:
            raise Exception("We have not detected the grabber. Plugin will exit...")

        if "hyperiond.sh" in subprocess.check_output("ps"):
            subprocess.call(["killall", "hyperiond"])

        cmd = "/storage/hyperion/bin/hyperion-v4l2.sh"
        if self.isOSMC:
            cmd = "hyperion-v4l2"

        if grabber == "utv007":
            print subprocess.check_output([cmd, "--video-standard", videoStandard, "--screenshot"])
        else:
            print(subprocess.check_output(
                [cmd, "--video-standard", videoStandard, "--width", "240", "--height", "192",
                 "--screenshot"]))

        return os.path.expanduser(os.path.join(path, "screenshot.png"))
