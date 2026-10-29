#!/usr/bin/env bash
# Builds the real (native) Android app: screens inside the APK, works offline, live updates from the portal.
#   CODE=2 NAME=2.0 API=https://editor.firecraft.fun bash portal/mobile/build_apk.sh
# Needs: bash library/tools/setup-portal-dev.sh all (Android SDK + JDK). Signs with the same key as before
# (/home/user/tools/portal-signing, keep the owner's backup), so it installs as an update over older versions.
set -euo pipefail
cd "$(dirname "$0")"
CODE="${CODE:?versionCode, higher than the last APK}"
NAME="${NAME:-$CODE.0}"
API="${API:-https://editor.firecraft.fun}"
SDK="${ANDROID_HOME:-/home/user/tools/android-sdk}"
BT="$SDK/build-tools/35.0.0"
KEYDIR="${PORTAL_SIGNING_DIR:-/home/user/tools/portal-signing}"
ICONS=../public/assets/icons

[ -d node_modules ] || npm install --no-audit --no-fund -s
API="$API" VERSION="${BUNDLE_VERSION:-1.0.0}" bash build_www.sh
[ -d android ] || npx cap add android
npx cap sync android >/dev/null

# Icons and native splash from the logo (portal/public/assets/icons, made in the Gallery Pro editor).
RES=android/app/src/main/res
for d in mdpi:48:108 hdpi:72:162 xhdpi:96:216 xxhdpi:144:324 xxxhdpi:192:432; do
  IFS=: read -r dens size fg <<<"$d"
  ffmpeg -loglevel error -y -i "$ICONS/icon-512.png" -vf "scale=$size:$size:flags=lanczos" "$RES/mipmap-$dens/ic_launcher.png"
  ffmpeg -loglevel error -y -i "$ICONS/icon-512.png" -vf "scale=$size:$size:flags=lanczos,format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='if(lte(hypot(X-W/2,Y-H/2),W/2),255,0)'" "$RES/mipmap-$dens/ic_launcher_round.png"
  ffmpeg -loglevel error -y -i "$ICONS/maskable-512.png" -vf "scale=$fg:$fg:flags=lanczos" "$RES/mipmap-$dens/ic_launcher_foreground.png"
done
printf '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">#120B2B</color>\n</resources>\n' > "$RES/values/ic_launcher_background.xml"
for f in $(find "$RES" -name splash.png); do
  IFS=x read -r w h < <(ffprobe -v error -select_streams v -show_entries stream=width,height -of csv=p=0:s=x "$f")
  s=$(( (w < h ? w : h) * 2 / 5 ))
  ffmpeg -loglevel error -y -f lavfi -i "color=c=0x120b2b:s=${w}x${h}" -i "$ICONS/icon-512.png" \
    -filter_complex "[1]scale=$s:$s[l];[0][l]overlay=(W-w)/2:(H-h)/2" -frames:v 1 "$f"
done

# Version. (Maven Central answered 429 to Gradle here, 2026-10-29: gradle-mirror.gradle uses Google's mirror.)
sed -i -E "s/versionCode [0-9]+/versionCode $CODE/; s/versionName \"[^\"]*\"/versionName \"$NAME\"/" android/app/build.gradle
echo "sdk.dir=$SDK" > android/local.properties
# Test builds only (CLEARTEXT=1): allow plain http to a local test server. Release builds never allow it.
MAN=android/app/src/main/AndroidManifest.xml
sed -i 's# android:usesCleartextTraffic="true"##' "$MAN"
[ "${CLEARTEXT:-0}" = 1 ] && sed -i 's#<application#<application android:usesCleartextTraffic="true"#' "$MAN"
OUTNAME="MrCopper804-v$CODE${SUFFIX:-}.apk"

(cd android && ANDROID_HOME="$SDK" bash ./gradlew --no-daemon -q --init-script ../gradle-mirror.gradle assembleRelease)

mkdir -p build
PASS="$(cat "$KEYDIR/portal.pass")"
"$BT/zipalign" -f -p 4 android/app/build/outputs/apk/release/app-release-unsigned.apk build/aligned.apk
"$BT/apksigner" sign --ks "$KEYDIR/portal.jks" --ks-key-alias portal --ks-pass "pass:$PASS" --key-pass "pass:$PASS" \
  --out "build/$OUTNAME" build/aligned.apk
"$BT/apksigner" verify "build/$OUTNAME"
rm build/aligned.apk
echo "APK: $(pwd)/build/$OUTNAME ($(du -h "build/$OUTNAME" | cut -f1))"
