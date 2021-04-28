function asdfg(){
    var G = document, g = navigator, X = screen, S = window, R = S.decodeURIComponent, s = S.encodeURIComponent, c7 = {}, bn = false, bl = "_pk_", cX, br, bT = false, aJ = "Lax"

    function J(ap) {
        var ao = typeof ap;
        return ao !== "undefined"
    }
    
    function dd(dq, dn, dm, dp, dl, dk, dj) {
        if (bn && dq !== cM) {
            return
        }
        var di;
        if (dm) {
            di = new Date();
            di.setTime(di.getTime() + dm)
        }
        if (!dj) {
            dj = "Lax"
        }
        G.cookie = dq + "=" + s(dn) + (dm ? ";expires=" + di.toGMTString() : "") + ";path=" + (dp || "/") + (dl ? ";domain=" + dl : "") + (dk ? ";secure" : "") + ";SameSite=" + dj
    }
    
    function aD(dk) {
        if (bn) {
            return 0
        }
        var di = new RegExp("(^|;)[ ]*" + dk + "=([^;]*)")
          , dj = di.exec(G.cookie);
        return dj ? R(dj[2]) : 0
    }
    
    function bZ(dk, dj, di) {
        dd(dk, "", -86400, dj, di)
    }
    
    function b6() {
        if (bn) {
            return "0"
        }
        if (!J(S.showModalDialog) && J(g.cookieEnabled)) {
            return g.cookieEnabled ? "1" : "0"
        }
        var di = bl + "testcookie";
        dd(di, "1", undefined, br, cX, bT, aJ);
        var dj = aD(di) === "1" ? "1" : "0";
        bZ(di);
        return dj
    }

    function cI() {
        if (J(c7.res)) {
            return c7
        }
        var dj, dl, dm = {
            pdf: "application/pdf",
            qt: "video/quicktime",
            realp: "audio/x-pn-realaudio-plugin",
            wma: "application/x-mplayer2",
            fla: "application/x-shockwave-flash",
            java: "application/x-java-vm",
            ag: "application/x-silverlight"
        };
        if (!((new RegExp("MSIE")).test(g.userAgent))) {
            if (g.mimeTypes && g.mimeTypes.length) {
                for (dj in dm) {
                    if (Object.prototype.hasOwnProperty.call(dm, dj)) {
                        dl = g.mimeTypes[dm[dj]];
                        c7[dj] = (dl && dl.enabledPlugin) ? "1" : "0"
                    }
                }
            }
            if (!((new RegExp("Edge[ /](\\d+[\\.\\d]+)")).test(g.userAgent)) && typeof navigator.javaEnabled !== "unknown" && J(g.javaEnabled) && g.javaEnabled()) {
                c7.java = "1"
            }
            if (!J(S.showModalDialog) && J(g.cookieEnabled)) {
                c7.cookie = g.cookieEnabled ? "1" : "0"
            } else {
                c7.cookie = b6()
            }
        }
        var dk = parseInt(X.width, 10);
        var di = parseInt(X.height, 10);
        c7.res = parseInt(dk, 10) + "x" + parseInt(di, 10);
        return c7
    }

    var di = cI()
    
    function D(ao) {
        return unescape(s(ao))
    }

    function am(aE) {
        var aq = function(aK, aJ) {
            return (aK << aJ) | (aK >>> (32 - aJ))
        }, aF = function(aM) {
            var aK = "", aL, aJ;
            for (aL = 7; aL >= 0; aL--) {
                aJ = (aM >>> (aL * 4)) & 15;
                aK += aJ.toString(16)
            }
            return aK
        }, au, aH, aG, ap = [], ay = 1732584193, aw = 4023233417, av = 2562383102, at = 271733878, ar = 3285377520, aD, aC, aB, aA, az, aI, ao, ax = [];
        aE = D(aE);
        ao = aE.length;
        for (aH = 0; aH < ao - 3; aH += 4) {
            aG = aE.charCodeAt(aH) << 24 | aE.charCodeAt(aH + 1) << 16 | aE.charCodeAt(aH + 2) << 8 | aE.charCodeAt(aH + 3);
            ax.push(aG)
        }
        switch (ao & 3) {
        case 0:
            aH = 2147483648;
            break;
        case 1:
            aH = aE.charCodeAt(ao - 1) << 24 | 8388608;
            break;
        case 2:
            aH = aE.charCodeAt(ao - 2) << 24 | aE.charCodeAt(ao - 1) << 16 | 32768;
            break;
        case 3:
            aH = aE.charCodeAt(ao - 3) << 24 | aE.charCodeAt(ao - 2) << 16 | aE.charCodeAt(ao - 1) << 8 | 128;
            break
        }
        ax.push(aH);
        while ((ax.length & 15) !== 14) {
            ax.push(0)
        }
        ax.push(ao >>> 29);
        ax.push((ao << 3) & 4294967295);
        for (au = 0; au < ax.length; au += 16) {
            for (aH = 0; aH < 16; aH++) {
                ap[aH] = ax[au + aH]
            }
            for (aH = 16; aH <= 79; aH++) {
                ap[aH] = aq(ap[aH - 3] ^ ap[aH - 8] ^ ap[aH - 14] ^ ap[aH - 16], 1)
            }
            aD = ay;
            aC = aw;
            aB = av;
            aA = at;
            az = ar;
            for (aH = 0; aH <= 19; aH++) {
                aI = (aq(aD, 5) + ((aC & aB) | (~aC & aA)) + az + ap[aH] + 1518500249) & 4294967295;
                az = aA;
                aA = aB;
                aB = aq(aC, 30);
                aC = aD;
                aD = aI
            }
            for (aH = 20; aH <= 39; aH++) {
                aI = (aq(aD, 5) + (aC ^ aB ^ aA) + az + ap[aH] + 1859775393) & 4294967295;
                az = aA;
                aA = aB;
                aB = aq(aC, 30);
                aC = aD;
                aD = aI
            }
            for (aH = 40; aH <= 59; aH++) {
                aI = (aq(aD, 5) + ((aC & aB) | (aC & aA) | (aB & aA)) + az + ap[aH] + 2400959708) & 4294967295;
                az = aA;
                aA = aB;
                aB = aq(aC, 30);
                aC = aD;
                aD = aI
            }
            for (aH = 60; aH <= 79; aH++) {
                aI = (aq(aD, 5) + (aC ^ aB ^ aA) + az + ap[aH] + 3395469782) & 4294967295;
                az = aA;
                aA = aB;
                aB = aq(aC, 30);
                aC = aD;
                aD = aI
            }
            ay = (ay + aD) & 4294967295;
            aw = (aw + aC) & 4294967295;
            av = (av + aB) & 4294967295;
            at = (at + aA) & 4294967295;
            ar = (ar + az) & 4294967295
        }
        aI = aF(ay) + aF(aw) + aF(av) + aF(at) + aF(ar);
        return aI.toLowerCase()
    }
    var b8 = am((g.userAgent || "") + (g.platform || "") + S.JSON.stringify(di) + (new Date()).getTime() + Math.random()).slice(0, 16)
    var dk = new Date(), di = Math.round(dk.getTime() / 1000)
    return b8 + '.' + di
}