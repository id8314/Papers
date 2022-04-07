from datetime import datetime

# Format seconds to days, hours, minutes and seconds string
def ptime(seconds):
    if(seconds >= 86400):
        d = seconds // 86400 # // floor division
        return (f"{round(d)}d") + ptime(seconds - d * 86400)
    else:
        if(seconds >= 3600):
            h = seconds // 3600 
            return (f"{round(h)}h") + ptime(seconds - h * 3600)
        else:
            if(seconds >= 60):
                m = seconds // 60
                return(f"{round(m)}m" + ptime(seconds - m * 60))
            else:
                if (seconds > 0):
                    return(f"{round(seconds)}s")
                else:
                    return("")

def now():
    return datetime.now().strftime("%H:%M:%S")
