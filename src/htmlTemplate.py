head = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
<head>

    <title>Rapport de configuration</title>
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />


    <style type="text/css">
        html{color:#000;background:#FFF;}body,div,dl,dt,dd,ul,ol,li,h1,h2,h3,h4,h5,h6,pre,code,form,fieldset,legend,input,button,textarea,p,blockquote,th,td{margin:0;padding:0;}table{border-collapse:collapse;border-spacing:0;}fieldset,img{border:0;}address,caption,cite,code,dfn,em,strong,th,var,optgroup{font-style:inherit;font-weight:inherit;}del,ins{text-decoration:none;}li{list-style:none;}caption,th{text-align:left;}h1,h2,h3,h4,h5,h6{font-size:100%;font-weight:normal;}q:before,q:after{content:'';}abbr,acronym{border:0;font-variant:normal;}sup{vertical-align:baseline;}sub{vertical-align:baseline;}legend{color:#000;}input,button,textarea,select,optgroup,option{font-family:inherit;font-size:inherit;font-style:inherit;font-weight:inherit;}input,button,textarea,select{*font-size:100%;}body{font:13px/1.231 arial,helvetica,clean,sans-serif;*font-size:small;*font:x-small;}select,input,button,textarea,button{font:99% arial,helvetica,clean,sans-serif;}table{font-size:inherit;font:100%;}pre,code,kbd,samp,tt{font-family:monospace;*font-size:108%;line-height:100%;}body{text-align:center;}#doc,#doc2,#doc3,#doc4,.yui-t1,.yui-t2,.yui-t3,.yui-t4,.yui-t5,.yui-t6,.yui-t7{margin:auto;text-align:left;width:57.69em;*width:56.25em;}#doc2{width:73.076em;*width:71.25em;}#doc3{margin:auto 10px;width:auto;}#doc4{width:74.923em;*width:73.05em;}.yui-b{position:relative;}.yui-b{_position:static;}#yui-main .yui-b{position:static;}#yui-main,.yui-g .yui-u .yui-g{width:100%;}.yui-t1 #yui-main,.yui-t2 #yui-main,.yui-t3 #yui-main{float:right;margin-left:-25em;}.yui-t4 #yui-main,.yui-t5 #yui-main,.yui-t6 #yui-main{float:left;margin-right:-25em;}.yui-t1 .yui-b{float:left;width:12.30769em;*width:12.00em;}.yui-t1 #yui-main .yui-b{margin-left:13.30769em;*margin-left:13.05em;}.yui-t2 .yui-b{float:left;width:13.8461em;*width:13.50em;}.yui-t2 #yui-main .yui-b{margin-left:14.8461em;*margin-left:14.55em;}.yui-t3 .yui-b{float:left;width:23.0769em;*width:22.50em;}.yui-t3 #yui-main .yui-b{margin-left:24.0769em;*margin-left:23.62em;}.yui-t4 .yui-b{float:right;width:13.8456em;*width:13.50em;}.yui-t4 #yui-main .yui-b{margin-right:14.8456em;*margin-right:14.55em;}.yui-t5 .yui-b{float:right;width:18.4615em;*width:18.00em;}.yui-t5 #yui-main .yui-b{margin-right:19.4615em;*margin-right:19.125em;}.yui-t6 .yui-b{float:right;width:23.0769em;*width:22.50em;}.yui-t6 #yui-main .yui-b{margin-right:24.0769em;*margin-right:23.62em;}.yui-t7 #yui-main .yui-b{display:block;margin:0 0 1em 0;}#yui-main .yui-b{float:none;width:auto;}.yui-gb .yui-u,.yui-g .yui-gb .yui-u,.yui-gb .yui-g,.yui-gb .yui-gb,.yui-gb .yui-gc,.yui-gb .yui-gd,.yui-gb .yui-ge,.yui-gb .yui-gf,.yui-gc .yui-u,.yui-gc .yui-g,.yui-gd .yui-u{float:left;}.yui-g .yui-u,.yui-g .yui-g,.yui-g .yui-gb,.yui-g .yui-gc,.yui-g .yui-gd,.yui-g .yui-ge,.yui-g .yui-gf,.yui-gc .yui-u,.yui-gd .yui-g,.yui-g .yui-gc .yui-u,.yui-ge .yui-u,.yui-ge .yui-g,.yui-gf .yui-g,.yui-gf .yui-u{float:right;}.yui-g div.first,.yui-gb div.first,.yui-gc div.first,.yui-gd div.first,.yui-ge div.first,.yui-gf div.first,.yui-g .yui-gc div.first,.yui-g .yui-ge div.first,.yui-gc div.first div.first{float:left;}.yui-g .yui-u,.yui-g .yui-g,.yui-g .yui-gb,.yui-g .yui-gc,.yui-g .yui-gd,.yui-g .yui-ge,.yui-g .yui-gf{width:49.1%;}.yui-gb .yui-u,.yui-g .yui-gb .yui-u,.yui-gb .yui-g,.yui-gb .yui-gb,.yui-gb .yui-gc,.yui-gb .yui-gd,.yui-gb .yui-ge,.yui-gb .yui-gf,.yui-gc .yui-u,.yui-gc .yui-g,.yui-gd .yui-u{width:32%;margin-left:1.99%;}.yui-gb .yui-u{*margin-left:1.9%;*width:31.9%;}.yui-gc div.first,.yui-gd .yui-u{width:66%;}.yui-gd div.first{width:32%;}.yui-ge div.first,.yui-gf .yui-u{width:74.2%;}.yui-ge .yui-u,.yui-gf div.first{width:24%;}.yui-g .yui-gb div.first,.yui-gb div.first,.yui-gc div.first,.yui-gd div.first{margin-left:0;}.yui-g .yui-g .yui-u,.yui-gb .yui-g .yui-u,.yui-gc .yui-g .yui-u,.yui-gd .yui-g .yui-u,.yui-ge .yui-g .yui-u,.yui-gf .yui-g .yui-u{width:49%;*width:48.1%;*margin-left:0;}.yui-g .yui-g .yui-u{width:48.1%;}.yui-g .yui-gb div.first,.yui-gb .yui-gb div.first{*margin-right:0;*width:32%;_width:31.7%;}.yui-g .yui-gc div.first,.yui-gd .yui-g{width:66%;}.yui-gb .yui-g div.first{*margin-right:4%;_margin-right:1.3%;}.yui-gb .yui-gc div.first,.yui-gb .yui-gd div.first{*margin-right:0;}.yui-gb .yui-gb .yui-u,.yui-gb .yui-gc .yui-u{*margin-left:1.8%;_margin-left:4%;}.yui-g .yui-gb .yui-u{_margin-left:1.0%;}.yui-gb .yui-gd .yui-u{*width:66%;_width:61.2%;}.yui-gb .yui-gd div.first{*width:31%;_width:29.5%;}.yui-g .yui-gc .yui-u,.yui-gb .yui-gc .yui-u{width:32%;_float:right;margin-right:0;_margin-left:0;}.yui-gb .yui-gc div.first{width:66%;*float:left;*margin-left:0;}.yui-gb .yui-ge .yui-u,.yui-gb .yui-gf .yui-u{margin:0;}.yui-gb .yui-gb .yui-u{_margin-left:.7%;}.yui-gb .yui-g div.first,.yui-gb .yui-gb div.first{*margin-left:0;}.yui-gc .yui-g .yui-u,.yui-gd .yui-g .yui-u{*width:48.1%;*margin-left:0;}.yui-gb .yui-gd div.first{width:32%;}.yui-g .yui-gd div.first{_width:29.9%;}.yui-ge .yui-g{width:24%;}.yui-gf .yui-g{width:74.2%;}.yui-gb .yui-ge div.yui-u,.yui-gb .yui-gf div.yui-u{float:right;}.yui-gb .yui-ge div.first,.yui-gb .yui-gf div.first{float:left;}.yui-gb .yui-ge .yui-u,.yui-gb .yui-gf div.first{*width:24%;_width:20%;}.yui-gb .yui-ge div.first,.yui-gb .yui-gf .yui-u{*width:73.5%;_width:65.5%;}.yui-ge div.first .yui-gd .yui-u{width:65%;}.yui-ge div.first .yui-gd div.first{width:32%;}#hd:after,#bd:after,#ft:after,.yui-g:after,.yui-gb:after,.yui-gc:after,.yui-gd:after,.yui-ge:after,.yui-gf:after{content:".";display:block;height:0;clear:both;visibility:hidden;}#hd,#bd,#ft,.yui-g,.yui-gb,.yui-gc,.yui-gd,.yui-ge,.yui-gf{zoom:1;}
        
        .msg { padding: 10px; background: #222; position: relative; }
        .msg h1 { color: #fff;  }
        .msg a { margin-left: 20px; background: #408814; color: white; padding: 4px 8px; text-decoration: none; }
        .msg a:hover { background: #266400; }

        /* //-- yui-grids style overrides -- */
        body { font-family: Georgia; color: #444; }
        #inner { padding: 10px 10px; margin: 10px auto; background: #ffffff; }
        .yui-gf { margin-bottom: 2em; padding-bottom: 2em; border-bottom: 1px solid #ccc; }

        /* //-- header, body, footer -- */
        #hd { margin: 2.5em 0 3em 0; padding-bottom: 1.5em; }
        #hd h2 { text-transform: uppercase; letter-spacing: 2px; }
        #bd, #ft { margin-bottom: 1em; }

        /* //-- footer -- */
        #ft { padding: 0em 0 1.5em 0; font-size: 92%; text-align: center; }
        #ft p { margin-bottom: 0; text-align: center;   }

        /* //-- core typography and style -- */
        #hd h1 { font-size: 48px; text-transform: uppercase; }
        h2 { font-size: 152% }
        h3, h4 { font-size: 122%; }
        h1, h2, h3, h4 { color: #333; }
        p { font-size: 100%; line-height: 18px; padding-right: 3em; }
        a { color: #990003 }
        a:hover { text-decoration: none; }
        strong { font-weight: bold; }
        li { line-height: 24px; border-bottom: 1px solid #ccc; }
        p.enlarge { font-size: 144%; padding-right: 6.5em; line-height: 24px; }
        p.enlarge span { color: #000 }
        .contact-info { margin-top: 7px; }
        .first h2 { font-style: italic; }
        .last { border-bottom: 0 }


        /* //-- section styles -- */

        a#pdf { display: block; float: left; background: #666; color: white; padding: 6px 50px 6px 12px; margin-bottom: 6px; text-decoration: none;  }
        a#pdf:hover { background: #222; }

        .job { position: relative; margin-bottom: 1em; padding-bottom: 1em; border-bottom: 1px solid #ccc; }
    .job:last-child { border: 0px; margin-bottom: 0em; }
        .job h4 { position: absolute; top: 0.35em; right: 0 }
        .job p { margin: 0.75em 0 0em 0; margin-left: 20px; }
        .job ul { margin-left: 20px; margin-top: 10px; margin-bottom: -10px;}
    .job ul li:last-child { border: 0px; }

        .last { border: none; }
        .skills-list {  }
        .skills-list ul { margin: 0; }
        .skills-list li { margin: 3px 0; padding: 3px 0; }
        .skills-list li span { font-size: 152%; display: block; margin-bottom: -2px; padding: 0 }
        .talent { width: 32%; float: left }
        .talent h2 { margin-bottom: 6px; }
    .talent li:last-child { border: 0px; }

        #srt-ttab { margin-bottom: 100px; text-align: center;  }
        #srt-ttab img.last { margin-top: 20px }

        /* --// override to force 1/8th width grids -- */
        .yui-gf .yui-u{width:80.2%;}
        .yui-gf div.first{width:12.3%;}
    </style>

</head>
<body>

<div id="doc2" class="yui-t7">
    <div id="inner">
    
        <div id="hd">
            <div class="yui-gc">
                <div class="yui-u first">
                    <img alt="" src="data:image/jpeg;base64,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" style="float: left; margin-left: -25px; margin-top: -35px;" />
                    <h1 style="font-size: 250%; text-align: center;" >Rapport <br/>de configuration</h1>
                    
                </div>

                <div class="yui-u">"""

def gen_top(data):
    html = """        <div class="contact-info">
                        <h3><a id="pdf" href="#"> ACIRPE """+transform_html(data,"get_acirpe_number")+"""</a></h3>
                        <br /><br /><br />
                        <h3>N° de série : """+transform_html(data,"get_serial_number")+""" </h3>
                    </div><!--// .contact-info -->"""
    return html

first_transition = """      </div>
            </div><!--// .yui-gc -->
        </div><!--// hd -->

        <div id="bd">
            <div id="yui-main">
                <div class="yui-b">

                    <div class="yui-gf">
                        <div class="yui-u first">
                            <h2>Résumé</h2>
                        </div>"""
                        
def gen_resume(data):
    html = """      <div class="yui-u">
                            <ul class="talent">
                                <li>Processeur</li>
                                <li>Mémoire Vive (RAM)</li>
                                <li>Capacité de stockage</li>
                                <li>Connectique USB</li>
                            </ul>

                            <ul class="talent">
                                <li>:</li>
                                <li>:</li>
                                <li>:</li>
                                <li>:</li>
                            </ul>

                            <ul class="talent">
                                <li>"""+transform_html(data,"get_cpu_speed")+""" [x"""+transform_html(data,"get_cpu_bits")+"""]</li>
                                <li>"""+transform_html(data,"get_memory_size")+"""</li>
                                <li>"""+transform_html(data,"get_disk_size")+"""</li>
                                <li>"""+transform_html(data,"get_usb_detail")+"""</li>
                            </ul>

                        </div>"""
    return html

second_transition = """                    </div><!--// .yui-gf -->
                    
                    <div class="yui-gf">
                        <div class="yui-u first">
                            <h2>Détail</h2>
                        </div><!--// .yui-u -->

                        <div class="yui-u">"""
 
def transform_html(data,cle):
    try:
        donnee = data[cle]
    except KeyError:
        return "???"
    html = ""
    if type(donnee) == list:
        if len(donnee) > 1:
            html = "<ul>\n"
            for elem in donnee:
                html += "<li>"+elem+"</li>\n"
            return html+"\n</ul>"
        else:
            return donnee[0]
#    elif donnee == "" or donnee == "???":
#        return "Impossible d'obtenir cette inforamtion depuis le système de l'ordinateur"
    else:
        return donnee
                        
def gen_detail(data):
    liste_detail = [["Processeur","cpu_detail"],["Mémoire vive","memory_detail"],["Disque dur","disk_detail"],["Carte graphique","video_detail"],["Carte son","multimedia_detail"],["Carte mère","mothercard_detail"]]
    html = ""
    for detail in liste_detail:
        if data.get("get_"+detail[1],"") in ("","???"):
            continue
        html += """<div class="job">
                                <h2>"""+detail[0]+"""</h2>
                                
                                <p>"""+transform_html(data,"get_"+detail[1])+"""</p>
                            </div>"""
    return html

feet = """</div><!--// .yui-u -->
                    </div>

                    <div class="yui-gf">
    
                        <div class="yui-u first">
                            <h2>Prix de revente</h2>
                        </div>
                        <div class="yui-u">
                            <p class="enlarge">
                              ***PRIX-DE-REVENTE***
                            </p>
                        </div>
                    </div><!--// .yui-gf -->



                </div><!--// .yui-b -->
            </div><!--// yui-main -->
        </div><!--// bd -->

        <div id="ft">
            <p> Pragraphe libre expliquant le pourquoi du comment : Intrinsicly enable optimal core competencies through corporate relationships. Phosfluorescently implement worldwide vortals and client-focused imperatives. Conveniently initiate virtual paradigms and top-line convergence.</p>
        </div><!--// footer -->

    </div><!-- // inner -->


</div><!--// doc -->


</body>
</html>"""