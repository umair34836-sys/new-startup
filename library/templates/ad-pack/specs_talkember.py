import json, os, sys
S = os.path.dirname(os.path.abspath(__file__))
END = lambda icons=True: {"cta": "app.talkember.site", "url2": "video.talkember.site", "icons": ["ChatGPT", "Google Flow", "YouTube"] if icons else []}
M = "cc0/"
ADS = [
 dict(id="01", lang="hi", style="s01", voice="viraj", music=M+"upbeat-electronic--loyalty-freak-music--people-are-spinning.mp3", music_start=19.0, title="Roz upload ki thakan", lines=[
  dict(say="रोज़ एक Short डालना... आसान लगता है?", h="Roz ek Short. Aasaan?", hi=["short"], vis=dict(type="chips", items=["Idea", "Script", "Video", "Captions", "Upload"])),
  dict(say="तीसरे दिन ही थकान शुरू हो जाती है।", h="Teesre din thakan shuru.", hi=["thakan"], vis=dict(type="big", text="Day 3", sub="aur channel ruk gaya")),
  dict(say="AI Video Automator ये पूरा काम रोज़ खुद करता है।", h="Ye poora kaam roz khud.", hi=["khud"], vis=dict(type="phone", img="autopilot.jpg")),
  dict(say="Idea से upload तक, आपके चुने वक़्त पर।", h="Idea se upload tak.", hi=["upload"], vis=dict(type="phone", img="autopilot_publish.jpg")),
  dict(say="आज ही शुरू करो: app dot talkember dot site।", h="Aaj hi shuru karo.", hi=["shuru"], end=END())]),
 dict(id="02", lang="hi", style="s02", voice="yash", music=M+"upbeat-electronic--holiznacc0--phonk-remix.mp3", title="PC band, kaam chalu", lines=[
  dict(say="Channel चलाने के लिए PC पूरा दिन on रखना पड़ता है?", h="PC poora din on?", hi=["pc"], vis=dict(type="big", text="24/7", sub="bijli, internet, tension")),
  dict(say="अब नहीं। AI Video Automator हमारे server पर चलता है।", h="Ab hamare server par.", hi=["server"], vis=dict(type="phone", img="accounts.jpg")),
  dict(say="आपका PC बंद हो, phone बंद हो, काम फिर भी चलता है।", h="PC band. Kaam chalu.", hi=["chalu"], vis=dict(type="chips", items=["PC off", "Phone off", "Autopilot ON"])),
  dict(say="बस एक बार अपने accounts connect करो।", h="Bas accounts connect karo.", hi=["connect"], vis=dict(type="chips", items=["ChatGPT", "Google Flow", "YouTube"])),
  dict(say="app dot talkember dot site पर आज ही शुरू करो।", h="Aaj hi shuru karo.", hi=["aaj"], end=END())]),
 dict(id="03", lang="hi", style="s03", voice="seva", music=M+"happy-upbeat--holiznacc0--poor-but-happy.mp3", title="Sirf 3 accounts", lines=[
  dict(say="Setup में घंटे नहीं लगते। सिर्फ तीन accounts चाहिए।", h="Sirf 3 accounts.", hi=["3"], vis=dict(type="big", text="3", sub="accounts, bas")),
  dict(say="ChatGPT, script के लिए।", h="ChatGPT: script.", hi=["chatgpt"], vis=dict(type="chips", items=["ChatGPT"])),
  dict(say="Google Flow, video के लिए।", h="Google Flow: video.", hi=["flow"], vis=dict(type="chips", items=["Google Flow"])),
  dict(say="और YouTube, upload के लिए।", h="YouTube: upload.", hi=["youtube"], vis=dict(type="chips", items=["YouTube"])),
  dict(say="एक बार login करो, बाकी काम app खुद करता है।", h="Ek baar login. Baaki app.", hi=["login"], vis=dict(type="phone", img="accounts.jpg")),
  dict(say="app dot talkember dot site।", h="Shuru karo.", hi=["shuru"], end=END())]),
 dict(id="04", lang="hi", style="s04", voice="viraj", music=M+"happy-upbeat--loyalty-freak-music--yippee.mp3", title="Channel ko samajhta hai", lines=[
  dict(say="हर channel अलग होता है। तो एक जैसा content क्यों?", h="Har channel alag hai!", hi=["alag"], vis=dict(type="big", text="?", sub="ek jaisa content kyun")),
  dict(say="Channel setup आपके videos और numbers पढ़ता है।", h="Channel setup padhta hai.", hi=["padhta"], vis=dict(type="phone", img="profile.jpg")),
  dict(say="Niche, viewers और भाषा समझता है।", h="Niche. Viewers. Bhasha.", hi=["niche"], vis=dict(type="chips", items=["Niche", "Viewers", "Bhasha"])),
  dict(say="और पंद्रह दिन का plan बनाकर देता है।", h="15 din ka plan!", hi=["15"], vis=dict(type="phone", img="strategy.jpg")),
  dict(say="आज ही try करो: app dot talkember dot site।", h="Aaj hi try karo!", hi=["try"], end=END())]),
 dict(id="05", lang="hi", style="s05", voice="yash", music=M+"electronic--monplaisir--free-to-use-13.mp3", title="Apna waqt chuno", lines=[
  dict(say="आपका channel किस वक़्त काम करे? आप चुनो।", h="Kis waqt kaam kare? Aap chuno.", hi=["chuno"], vis=dict(type="phone", img="autopilot.jpg")),
  dict(say="Shift शुरू, सुबह नौ बजे। Shift ख़त्म, रात नौ बजे।", h="Shift: 09:00 se 21:00", hi=["0900", "2100"], vis=dict(type="big", text="09-21", sub="roz ki shift")),
  dict(say="रोज़ कितनी videos, और public या private, सब आपकी मर्ज़ी।", h="Roz kitni videos? Public ya private?", hi=["public", "private"], vis=dict(type="phone", img="autopilot_publish.jpg")),
  dict(say="Autopilot on करो, और भूल जाओ।", h="Autopilot ON. Bhool jao.", hi=["on"], vis=dict(type="chips", items=["Autopilot ON"])),
  dict(say="app dot talkember dot site।", h="app.talkember.site", hi=[], end=END())]),
 dict(id="06", lang="hi", style="s06", voice="sia", music=M+"happy-upbeat--loyalty-freak-music--sunglasses.mp3", title="Trends pakdo", lines=[
  dict(say="आज क्या चल रहा है, ये ढूँढने में ही आधा दिन निकल जाता है।", h="Aaj kya chal raha hai?", hi=["kya"], vis=dict(type="big", text="???", sub="trend dhoondte dhoondte")),
  dict(say="AI Video Automator आपके niche के इस हफ़्ते के trends खुद देखता है।", h="Is hafte ke trends, khud.", hi=["trends"], vis=dict(type="phone", img="strategy.jpg")),
  dict(say="फिर उसी पर idea और hook लिखता है।", h="Phir idea + hook.", hi=["hook"], vis=dict(type="chips", items=["Trend", "Idea", "Hook"])),
  dict(say="और video बनाकर upload भी कर देता है।", h="Video bana ke upload.", hi=["upload"], vis=dict(type="phone", img="autopilot.jpg")),
  dict(say="app dot talkember dot site पर शुरू करो।", h="Shuru karo!", hi=["shuru"], end=END())]),
 dict(id="07", lang="hi", style="s07", voice="shveta", music=M+"electronic--monplaisir--bonsoir.mp3", title="Fact check", lines=[
  dict(say="एक ग़लत fact, और comments में मज़ाक बन जाता है।", h="Ek galat fact, aur mazaak.", hi=["galat"], vis=dict(type="big", text="X", sub="galat jaankari")),
  dict(say="इसलिए AI Video Automator video बनाने से पहले facts check करता है।", h="Video se pehle fact check.", hi=["fact", "check"], vis=dict(type="chips", items=["Script", "Fact check", "Video"])),
  dict(say="चाहो तो script पहले आपसे approve भी करवाता है।", h="Chaho to script approve karo.", hi=["approve"], vis=dict(type="phone", img="settings.jpg")),
  dict(say="भरोसे वाला content, रोज़।", h="Bharose wala content, roz.", hi=["bharose"], vis=dict(type="chips", items=["Roz", "Sahi facts"])),
  dict(say="app dot talkember dot site।", h="app.talkember.site", hi=[], end=END())]),
 dict(id="08", lang="hi", style="s08", voice="viraj", music=M+"electronic--monplaisir--yellow-star.mp3", title="Roz ki report", lines=[
  dict(say="आज video गई या नहीं? Views कैसे हैं?", h="Video gayi? Views?", hi=["views"], vis=dict(type="big", text="?", sub="roz ka sawaal")),
  dict(say="रोज़ एक e-mail में पूरी report मिलती है।", h="Roz ki report e-mail par.", hi=["report"], vis=dict(type="chips", items=["Gmail"])),
  dict(say="आज की video, शुरुआती numbers, और क्या बेहतर करना है।", h="Video. Numbers. Kya behtar karein.", hi=["numbers"], vis=dict(type="steps", items=["Aaj ki video", "Shuruati numbers", "Kya behtar karna hai"])),
  dict(say="App खोलने की भी ज़रूरत नहीं।", h="App kholna bhi zaroori nahi.", hi=["nahi"], vis=dict(type="phone", img="autopilot_mail.jpg")),
  dict(say="app dot talkember dot site।", h="Shuru karo", hi=["shuru"], end=END())]),
 dict(id="09", lang="hi", style="s20", voice="yash", music=M+"happy-upbeat--loyalty-freak-music--go-to-the-picnic.mp3", title="Rs 33 roz", lines=[
  dict(say="एक editor रखोगे तो महीने का कितना खर्चा?", h="Editor ka kharcha?", hi=["kharcha"], vis=dict(type="big", text="Rs ???", sub="har mahine")),
  dict(say="AI Video Automator, सिर्फ़ तैंतीस रुपये रोज़।", h="Sirf Rs 33 roz.", hi=["33"], vis=dict(type="big", text="Rs 33", sub="roz (30 din ka plan)")),
  dict(say="एक दिन का plan सौ रुपये। पंद्रह दिन पाँच सौ। तीस दिन एक हज़ार।", h="Plans", hi=["plans"], vis=dict(type="steps", items=["1 din: Rs 100", "15 din: Rs 500", "30 din: Rs 1,000", "1 saal: Rs 10,000"])),
  dict(say="JazzCash, Easypaisa, SadaPay या UPaisa से pay करो।", h="Pay karna aasaan.", hi=["aasaan"], vis=dict(type="chips", items=["JazzCash", "Easypaisa", "SadaPay", "UPaisa"])),
  dict(say="Key लो video dot talkember dot site से।", h="Key yahan se lo.", hi=["key"], end=dict(cta="video.talkember.site", url2="app.talkember.site", icons=[]))]),
 dict(id="10", lang="hi", style="s09", voice="viraj", music=M+"upbeat-electronic--loyalty-freak-music--high-technologic-beat-explosion.mp3", music_start=46.7, title="Free tools se chalta hai", lines=[
  dict(say="महंगे AI subscriptions चाहिए? नहीं।", h="> mehnge subscriptions? nahi.", hi=["nahi"], vis=dict(type="big", text="Rs 0", sub="tools ka kharcha")),
  dict(say="ChatGPT का free plan भी चलता है।", h="> ChatGPT free plan: OK", hi=["ok"], vis=dict(type="chips", items=["ChatGPT"])),
  dict(say="Google Flow रोज़ पचास free credits देता है।", h="> Google Flow: 50 free credits roz", hi=["50"], vis=dict(type="phone", img="accounts_plan.jpg")),
  dict(say="और एक Short के लिए इतने काफ़ी हैं।", h="> 1 Short ke liye kaafi", hi=["kaafi"], vis=dict(type="big", text="50", sub="credits = 1 Short")),
  dict(say="app dot talkember dot site।", h="> app.talkember.site", hi=[], end=END())]),
 dict(id="11", lang="hi", style="s10", voice="seva", music=M+"electronic--monplaisir--rd2doom.mp3", title="Masla hal karein", lines=[
  dict(say="Internet slow हुआ, और video बीच में अटक गई।", h="Video beech mein atak gayi.", hi=["atak"], vis=dict(type="big", text="STOP", sub="internet slow")),
  dict(say="घबराओ मत। मसला हल करें में सब दिखता है।", h="Masla hal karein.", hi=["hal"], vis=dict(type="phone", img="masla.jpg")),
  dict(say="एक button दबाओ: दोबारा try करो।", h="Ek button: dobara try.", hi=["dobara"], vis=dict(type="chips", items=["Dobara try karo", "Aage chalao", "Login karo"])),
  dict(say="जो हिस्सा बन चुका है, वो दोबारा नहीं बनता।", h="Bana hua hissa dobara nahi banta.", hi=["nahi"], vis=dict(type="steps", items=["Script: bani hui", "Clips: bani hui", "Sirf baaki kaam"])),
  dict(say="app dot talkember dot site।", h="Shuru karo.", hi=["shuru"], end=END())]),
 dict(id="12", lang="hi", style="s11", voice="shveta", music=M+"electronic--monplaisir--dome-of-grey.mp3", title="Series aur lambi videos", lines=[
  dict(say="सिर्फ़ Shorts नहीं। लंबी videos भी।", h="Sirf Shorts nahi.", hi=["nahi"], vis=dict(type="chips", items=["30 sec", "1 min", "2 min", "3 min", "5 min"])),
  dict(say="तीस second से पाँच minute तक, जो चाहो।", h="30 sec se 5 min tak.", hi=["5"], vis=dict(type="phone", img="video_banao.jpg")),
  dict(say="एक कहानी, या पूरी series: part एक, दो, तीन।", h="Ek kahani ya poori series.", hi=["series"], vis=dict(type="steps", items=["Part 1", "Part 2", "Part 3"])),
  dict(say="बस लिखो क्या video चाहिए।", h="Bas likho kya chahiye.", hi=["likho"], vis=dict(type="phone", img="video_banao.jpg")),
  dict(say="app dot talkember dot site।", h="Aaj hi banao.", hi=["banao"], end=END())]),
 dict(id="13", lang="hi", style="s12", voice="sia", music=M+"happy-upbeat--john-bartmann--happy-clappy.mp3", title="Naya channel", lines=[
  dict(say="नया channel है, और समझ नहीं आ रहा क्या बनाएँ?", h="Naya channel? Kya banayein?", hi=["naya"], vis=dict(type="big", text="0", sub="videos abhi tak")),
  dict(say="AI Video Automator इस हफ़्ते के trends देखकर रास्ते बताता है।", h="Trends dekh kar raaste batata hai.", hi=["raaste"], vis=dict(type="steps", items=["Raasta 1", "Raasta 2", "Raasta 3"])),
  dict(say="आपसे कुछ छोटे सवाल पूछता है।", h="Kuch chhote sawaal.", hi=["sawaal"], vis=dict(type="phone", img="profile2.jpg")),
  dict(say="और फिर रोज़ video बनाना शुरू।", h="Phir roz video shuru.", hi=["roz"], vis=dict(type="phone", img="autopilot.jpg")),
  dict(say="app dot talkember dot site।", h="Shuruaat yahan se.", hi=["yahan"], end=END())]),
 dict(id="14", lang="hi", style="s13", voice="yash", music=M+"happy-upbeat--loyalty-freak-music--everyone-is-so-alive.mp3", title="Control aap ka", lines=[
  dict(say="Autopilot का मतलब ये नहीं कि control चला गया।", h="Control aap ke paas.", hi=["control"], vis=dict(type="big", text="100%", sub="aap ka control")),
  dict(say="चाहो तो video खुद publish हो।", h="Khud publish.", hi=["publish"], vis=dict(type="phone", img="autopilot_publish.jpg")),
  dict(say="चाहो तो पहले आपसे पूछे।", h="Ya pehle aap se pooche.", hi=["pooche"], vis=dict(type="chips", items=["Pehle mujh se poocho"])),
  dict(say="या private draft में रखे।", h="Ya private draft.", hi=["private"], vis=dict(type="chips", items=["Private draft"])),
  dict(say="Channel आपका, फ़ैसला आपका। app dot talkember dot site।", h="Channel aap ka. Faisla aap ka.", hi=["faisla"], end=END())]),
 dict(id="15", lang="hi", style="s14", voice="shveta", music=M+"desi-eastern--orient-peace-valley.mp3", title="Phone se chalao", lines=[
  dict(say="Laptop नहीं है? कोई बात नहीं।", h="Laptop nahi? Koi baat nahi.", hi=["nahi"], vis=dict(type="big", text="0", sub="laptop chahiye")),
  dict(say="AI Video Automator phone के browser में खुलता है।", h="Phone ke browser mein.", hi=["phone"], vis=dict(type="phone", img="accounts.jpg")),
  dict(say="वहीं से login, वहीं से autopilot।", h="Wahin login. Wahin autopilot.", hi=["autopilot"], vis=dict(type="phone", img="autopilot.jpg")),
  dict(say="और video बनती है हमारे server पर।", h="Video banti hai server par.", hi=["server"], vis=dict(type="chips", items=["Aap ka phone", "Hamara server"])),
  dict(say="app dot talkember dot site।", h="Abhi kholo.", hi=["kholo"], end=END())]),
 dict(id="16", lang="en", style="s17", voice="noah", music=M+"upbeat-electronic--loyalty-freak-music--monarch-of-the-street.mp3", title="Your channel on autopilot", lines=[
  dict(say="What if your YouTube channel posted every single day... without you?", h="A Short every day. Without you.", hi=["every", "day"], vis=dict(type="big", text="365", sub="days a year")),
  dict(say="AI Video Automator studies your channel.", h="It studies your channel.", hi=["studies"], vis=dict(type="phone", img="profile.jpg")),
  dict(say="Writes the script, makes the video, adds captions.", h="Script. Video. Captions.", hi=["captions"], vis=dict(type="chips", items=["Script", "Video", "Captions"])),
  dict(say="And uploads it, at the time you choose.", h="Uploaded at your time.", hi=["your"], vis=dict(type="phone", img="autopilot.jpg")),
  dict(say="Your channel, on autopilot. app dot talkember dot site.", h="Your channel, on autopilot.", hi=["autopilot"], end=END())]),
 dict(id="17", lang="en", style="s16", voice="skylar", music=M+"electronic--monplaisir--the-break.mp3", title="No PC needed", lines=[
  dict(say="You don't need a PC running all day.", h="No PC running all day.", hi=["no"], vis=dict(type="big", text="0", sub="PCs needed")),
  dict(say="AI Video Automator now runs on our server.", h="It runs on our server.", hi=["server"], vis=dict(type="phone", img="accounts.jpg")),
  dict(say="Connect ChatGPT, Google Flow and YouTube once.", h="Connect three accounts. Once.", hi=["once"], vis=dict(type="chips", items=["ChatGPT", "Google Flow", "YouTube"])),
  dict(say="Then close the tab. The work keeps going.", h="Close the tab. It keeps going.", hi=["keeps"], vis=dict(type="phone", img="autopilot.jpg")),
  dict(say="Start today at app dot talkember dot site.", h="Start today.", hi=["today"], end=END())]),
 dict(id="18", lang="en", style="s18", voice="noah", music=M+"electronic--monplaisir--the-call-part-1.mp3", title="How it works", lines=[
  dict(say="Four steps. That's the whole setup.", h="Four steps. That's it.", hi=["four"], vis=dict(type="big", text="4", sub="steps")),
  dict(say="One: sign in with your licence key.", h="1. Sign in with your key.", hi=["1"], vis=dict(type="steps", items=["Sign in with your key"])),
  dict(say="Two: connect ChatGPT, Google Flow and YouTube.", h="2. Connect your accounts.", hi=["2"], vis=dict(type="chips", items=["ChatGPT", "Google Flow", "YouTube"])),
  dict(say="Three: let it study your channel.", h="3. Channel check.", hi=["3"], vis=dict(type="phone", img="profile.jpg")),
  dict(say="Four: turn on Autopilot, and get a Short every day.", h="4. Autopilot on.", hi=["4"], vis=dict(type="phone", img="autopilot.jpg")),
  dict(say="app dot talkember dot site.", h="Try it today.", hi=["today"], end=END())]),
 dict(id="19", lang="en", style="s19", voice="skylar", music=M+"upbeat-electronic--loyalty-freak-music--you-know-why.mp3", title="The honest ad", lines=[
  dict(say="An honest ad. No software can promise you views.", h="No software can promise views.", hi=["no"], vis=dict(type="big", text="0", sub="fake promises")),
  dict(say="We don't either.", h="We don't either.", hi=["dont"], vis=dict(type="chips", items=["No views promised", "No income promised"])),
  dict(say="What AI Video Automator does: the daily work.", h="What it does: the daily work.", hi=["daily", "work"], vis=dict(type="steps", items=["Idea and script", "Video and captions", "Upload"])),
  dict(say="And a report every day: what happened, and what to improve.", h="Plus a daily report.", hi=["report"], vis=dict(type="phone", img="autopilot_mail.jpg")),
  dict(say="You stay in control. app dot talkember dot site.", h="You stay in control.", hi=["control"], end=END())]),
 dict(id="20", lang="en", style="s15", voice="noah", music=M+"happy-upbeat--loyalty-freak-music--it-feels-good-to-be-alive-too.mp3", title="Try it for a day", lines=[
  dict(say="Not sure? Try it for one full day.", h="Try it for one day!", hi=["one", "day"], vis=dict(type="big", text="1 DAY", sub="a full day")),
  dict(say="One hundred rupees. That's it.", h="Rs 100. That's it!", hi=["100"], vis=dict(type="big", text="Rs 100", sub="1 day plan")),
  dict(say="Like it? Thirty days is one thousand rupees.", h="30 days: Rs 1,000", hi=["1000"], vis=dict(type="steps", items=["1 day: Rs 100", "15 days: Rs 500", "30 days: Rs 1,000", "1 year: Rs 10,000"])),
  dict(say="Pay with JazzCash, Easypaisa, SadaPay or UPaisa.", h="Easy to pay!", hi=["easy"], vis=dict(type="chips", items=["JazzCash", "Easypaisa", "SadaPay", "UPaisa"])),
  dict(say="Get your key at video dot talkember dot site.", h="Get your key!", hi=["key"], end=dict(cta="video.talkember.site", url2="app.talkember.site", icons=[]))]),
]
if __name__ == "__main__":
    for ad in ADS:
        d = f"{S}/{ad['id']}"
        os.makedirs(d, exist_ok=True)
        ad["vo"] = f"{d}/vo.mp3"
        json.dump(ad, open(f"{d}/spec.json", "w"), ensure_ascii=False, indent=1)
        open(f"{d}/say.txt", "w").write("\n".join(l["say"] for l in ad["lines"]))
    print(len(ADS), "specs")
