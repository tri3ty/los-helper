(function(){"use strict";var t={3354:function(t,e,s){var r=s(9242),a=s(407),i=s.n(a),n=s(3396),o=s(7139);const l={class:"wrapper columns"},c={class:"column"},p={class:"box"},u={class:"stat"},h={class:"stat"},_={class:"stat"},d={class:"box"},f=(0,n._)("strong",null,"Recent State",-1),v={class:"stat"},w={class:"stat"},g={class:"stat"},m={class:"stat"},k={class:"stat"},z={class:"stat"},b={class:"stat"},y={class:"box"},x=(0,n._)("strong",null,"Juicy reporting...",-1),D={class:"stat"},O={class:"stat"},M={class:"stat"},S={class:"stat"},T={class:"stat"},j={class:"stat"},A={class:"stat"},C={class:"stat"},P={class:"stat"},E={class:"stat"},R={class:"stat"},H={class:"stat"},I={class:"stat"},K={class:"stat"},N={class:"stat"},Y={class:"stat"},q={class:"box"},F=(0,n._)("strong",null,"Paper doll...",-1),W={class:"stat"},B={class:"stat"},J={class:"stat"},L={class:"box"},G=(0,n._)("strong",null,"Stats...",-1),X={class:"stat"},Q={class:"box"},U=(0,n._)("strong",null,"Debug stuff...",-1),Z={class:"stat"},V={class:"stat"},$={class:"stat"},tt={class:"stat"},et={class:"stat"},st={class:"stat"},rt={class:"stat"},at={class:"stat"},it={class:"column is-half"},nt={class:"box"},ot=(0,n._)("strong",null,"Tracks run...",-1),lt={class:"table is-fullwidth"},ct=(0,n._)("tr",null,[(0,n._)("th",{title:"Active Track"}),(0,n._)("th",null,"Name"),(0,n._)("th",{title:"Runs"},"R"),(0,n._)("th",{title:"Abandons"},"A"),(0,n._)("th",{title:"Completes"},"C"),(0,n._)("th",null,"Exp"),(0,n._)("th",{title:"Exp per minute"},"Expm"),(0,n._)("th",{title:"Kills"},"K"),(0,n._)("th",{title:"Duration in minutes"},"D")],-1),pt={key:0},ut={key:1},ht={class:"box"},_t=(0,n._)("strong",null,"Physical damage...",-1),dt={class:"box"},ft=(0,n._)("strong",null,"Spell damage...",-1),vt={class:"box"},wt=(0,n._)("strong",null,"Equipment...",-1),gt={class:"stat"},mt={key:0,class:"stat"},kt={class:"stat"},zt={class:"stat"},bt={class:"box"},yt=(0,n._)("strong",null,"Inventory...",-1),xt={class:"table is-fullwidth"},Dt=(0,n._)("tr",null,[(0,n._)("th",null,"Name"),(0,n._)("th",null,"Quantity")],-1),Ot={class:"column"},Mt={class:"box"},St=(0,n._)("strong",null,"Mobs killed...",-1),Tt={class:"box"},jt=(0,n._)("strong",null,"Mobs targetted...",-1);function At(t,e,s,r,a,i){const At=(0,n.up)("apexchart");return(0,n.wg)(),(0,n.iD)("div",l,[(0,n._)("div",c,[(0,n._)("div",p,[(0,n._)("strong",null,(0,o.zw)(t.info.name)+" the "+(0,o.zw)(t.info.race)+" "+(0,o.zw)(i.classname),1),(0,n._)("div",u,"Level "+(0,o.zw)(t.info.level),1),(0,n._)("div",h,"HP "+(0,o.zw)(t.report.hp)+" / "+(0,o.zw)(t.info.hp),1),(0,n._)("div",_,"MP "+(0,o.zw)(t.report.mp)+" / "+(0,o.zw)(t.info.mp),1)]),(0,n._)("div",d,[f,(0,n._)("div",v,"As of "+(0,o.zw)(t.report.timestamp),1),(0,n._)("div",w,"Fighting "+(0,o.zw)(t.report.mobs),1),(0,n._)("div",g,"Area "+(0,o.zw)(t.report.area),1),(0,n._)("div",m,"Total runtime "+(0,o.zw)(t.report.runtime),1),(0,n._)("div",k,"Resting "+(0,o.zw)(t.report.percent_rest)+"% of the time",1),(0,n._)("div",z,"Tracking "+(0,o.zw)(t.report.percent_track)+"% of the time",1),(0,n._)("div",b,"Fighting "+(0,o.zw)(t.report.percent_combat)+"% of the time",1)]),(0,n._)("div",y,[x,(0,n._)("div",D,"Current Aura: "+(0,o.zw)(t.report.aura),1),(0,n._)("div",O,"EXP/Min: "+(0,o.zw)(t.report.expm)+" ("+(0,o.zw)(this.exph)+"/hr)",1),(0,n._)("div",M,"Exp Gained: "+(0,o.zw)(t.report.exp),1),(0,n._)("div",S,"Hit Rate (Phys): "+(0,o.zw)(t.report.phys_hit_rate)+"%",1),(0,n._)("div",T,"Avg Dmg (Phys): "+(0,o.zw)(t.report.average_phys_damage)+" ("+(0,o.zw)(i.effective_phys)+")",1),(0,n._)("div",j,"Crit Rate (attack): "+(0,o.zw)(i.crit_to_attack)+"%",1),(0,n._)("div",A,"Crit Rate (hit): "+(0,o.zw)(i.crit_to_hit)+"%",1),(0,n._)("div",C,"Attack/Hit/Crit: "+(0,o.zw)(t.report.total_phys_attacks)+"/"+(0,o.zw)(t.report.total_phys_hits)+"/"+(0,o.zw)(t.report.phys_crits),1),(0,n._)("div",P,"Hit Rate (Spell): "+(0,o.zw)(t.report.spell_hit_rate)+"%",1),(0,n._)("div",E,"Avg Dmg (Spell): "+(0,o.zw)(t.report.average_spell_damage)+" ("+(0,o.zw)(i.effective_spell)+")",1),(0,n._)("div",R,"Crit Rate (cast): "+(0,o.zw)(i.crit_to_cast)+"%",1),(0,n._)("div",H,"Crit Rate (hit): "+(0,o.zw)(i.crit_to_cast_hit)+"%",1),(0,n._)("div",I,"Cast/Hit/Crit: "+(0,o.zw)(t.report.spells_cast)+"/"+(0,o.zw)(t.report.spells_hit)+"/"+(0,o.zw)(t.report.spell_crits),1),(0,n._)("div",K,"Total KILLS: "+(0,o.zw)(i.total_kills),1),(0,n._)("div",N,"KPM: "+(0,o.zw)(this.kpm),1),(0,n._)("div",Y,"DEATHS "+(0,o.zw)(t.report.deaths),1)]),(0,n._)("div",q,[F,(0,n._)("div",W,"Preferred Aura: "+(0,o.zw)(t.info.preferred_aura),1),(0,n._)("div",B,"Exp: "+(0,o.zw)(i.experience),1),(0,n._)("div",J,"Exp To Level: "+(0,o.zw)(t.info.exp_to_level),1)]),(0,n._)("div",L,[G,(0,n.Wm)(At,{width:"250",type:"radar",options:t.statOptions,series:i.statSeries},null,8,["options","series"]),((0,n.wg)(!0),(0,n.iD)(n.HY,null,(0,n.Ko)(t.info.stats,(t=>((0,n.wg)(),(0,n.iD)("div",{class:"stats",key:t.name},[(0,n._)("div",X,(0,o.zw)(t.name)+" "+(0,o.zw)(t.value),1)])))),128))]),(0,n._)("div",Q,[U,(0,n._)("div",Z,"Last Direction: "+(0,o.zw)(t.report.last_direction),1),(0,n._)("div",V,"Sucessful Go: "+(0,o.zw)(t.report.successful_go),1),(0,n._)("div",$,"Blocking Mob: ["+(0,o.zw)(t.report.blocking_mob)+"]",1),(0,n._)("div",tt,"Please Wait: "+(0,o.zw)(t.report.go_please_wait),1),(0,n._)("div",et,"No Exit: "+(0,o.zw)(t.report.go_no_exit),1),(0,n._)("div",st,"Timeout: "+(0,o.zw)(t.report.go_timeout),1),(0,n._)("div",rt,"Confused: "+(0,o.zw)(t.report.confused),1),(0,n._)("div",at,"Can See: "+(0,o.zw)(t.report.can_see),1)])]),(0,n._)("div",it,[(0,n._)("div",nt,[ot,(0,n._)("table",lt,[ct,((0,n.wg)(!0),(0,n.iD)(n.HY,null,(0,n.Ko)(this.sorted_tracks,(e=>((0,n.wg)(),(0,n.iD)("tr",{key:e.name},[e.name==t.report.track?((0,n.wg)(),(0,n.iD)("td",pt,"*")):((0,n.wg)(),(0,n.iD)("td",ut)),(0,n._)("td",null,(0,o.zw)(e.name),1),(0,n._)("td",null,(0,o.zw)(e.runs),1),(0,n._)("td",null,(0,o.zw)(e.abandons),1),(0,n._)("td",null,(0,o.zw)(e.completes),1),(0,n._)("td",null,(0,o.zw)(e.exp),1),(0,n._)("td",null,(0,o.zw)(i.processExpm(e))+"/min",1),(0,n._)("td",null,(0,o.zw)(e.kills),1),(0,n._)("td",null,(0,o.zw)(Math.floor(e.duration/60*100)/100),1)])))),128))])]),(0,n._)("div",ht,[_t,(0,n.Wm)(At,{width:"500",type:"bar",options:i.attackOptions,series:i.attackSeries},null,8,["options","series"])]),(0,n._)("div",dt,[ft,(0,n.Wm)(At,{width:"500",type:"bar",options:i.castOptions,series:i.castSeries},null,8,["options","series"])]),(0,n._)("div",vt,[wt,(0,n._)("div",gt,"Wielded: ["+(0,o.zw)(t.report.weapon1)+"]",1),""!=t.report.weapon2?((0,n.wg)(),(0,n.iD)("div",mt,"Wielded: "+(0,o.zw)(t.report.weapon2),1)):(0,n.kq)("",!0),((0,n.wg)(!0),(0,n.iD)(n.HY,null,(0,n.Ko)(t.equipment,((t,e,s)=>((0,n.wg)(),(0,n.iD)("div",{key:s},[(0,n._)("div",kt,(0,o.zw)(t),1),(0,n._)("div",zt,(0,o.zw)(e),1)])))),128))]),(0,n._)("div",bt,[yt,(0,n._)("table",xt,[Dt,((0,n.wg)(!0),(0,n.iD)(n.HY,null,(0,n.Ko)(t.report.inventory,((t,e)=>((0,n.wg)(),(0,n.iD)("tr",{key:e},[(0,n._)("td",null,(0,o.zw)(e),1),(0,n._)("td",null,(0,o.zw)(t),1)])))),128))])])]),(0,n._)("div",Ot,[(0,n._)("div",Mt,[St,((0,n.wg)(!0),(0,n.iD)(n.HY,null,(0,n.Ko)(i.mobs_killed,((t,e)=>((0,n.wg)(),(0,n.iD)("div",{key:e},(0,o.zw)(t)+" "+(0,o.zw)(e),1)))),128))]),(0,n._)("div",Tt,[jt,((0,n.wg)(!0),(0,n.iD)(n.HY,null,(0,n.Ko)(i.sorted_mkl,(t=>((0,n.wg)(),(0,n.iD)("div",{key:t},(0,o.zw)(t),1)))),128))])])])}var Ct=s(6265),Pt=s.n(Ct),Et={name:"App",data:function(){return{mkl:[],info:{},report:{},track_report:[],equipment:{body:"",arms:"",legs:"",neck:"",neck2:"",hands:"",head:"",feet:"",face:"",finger:"",finger2:"",finger3:"",finger4:"",finger5:"",finger6:"",finger7:"",finger8:"",shield:"",wielded:null,seconded:null,holding:null},pollInterval:"",status:"",darkMode:!0,statOptions:{chart:{id:"stat-chart"},xaxis:{categories:["STR","DEX","CON","INT","PTY"]}},attackOptionsTemp:{chart:{id:"attack-chart"},yaxis:{categories:["0","10"]},xaxis:{tickAmount:20}},series:[{name:"series-1",data:[18,18,3,18,3]}]}},created(){this.fetchData(),this.pollInterval=setInterval(this.fetchData,3e4)},beforeUnmount(){clearInterval(this.pollInterval)},methods:{fetchData:function(){console.log("here I go fetching data again..."),Pt().get("api/mkl.json?t="+(new Date).getTime()).then((t=>{this.mkl=t.data})),Pt().get("../api/info.json?t="+(new Date).getTime()).then((t=>{this.info=t.data})),Pt().get("../api/report.json?t="+(new Date).getTime()).then((t=>{this.report=t.data})),Pt().get("../api/track_report.json?t="+(new Date).getTime()).then((t=>{this.track_report=t.data})),Pt().get("../api/equipment.json?t="+(new Date).getTime()).then((t=>{this.equipment=t.data}))},processExpm:function(t){var e=1,s=0;return t.duration&&0!==t.duration?(e=parseFloat(t.duration)/60,t.exp&&0!=t.exp&&(s=t.exp),Math.floor(s/e)):0}},watch:{},computed:{attackOptions:function(){let t=this.attackOptionsTemp;if(this.report!=={}&&this.report.attacks){let e=Object.keys(this.report.attacks["p"]);t={chart:{id:"attack-chart"},xaxis:{categories:e}}}return t},attackSeries:function(){let t=[{name:"hits",data:[0]}],e=[];if(this.report&&this.report.attacks){for(var s=0;s<Object.keys(this.report.attacks["p"]).length;s++){let t=Object.keys(this.report.attacks["p"])[s],r=this.report.attacks["p"][t];e.push(r)}t=[{name:"hits",data:e}]}return t},castOptions:function(){let t=this.attackOptionsTemp;if(this.report!=={}&&this.report.attacks){let e=Object.keys(this.report.attacks["s"]);t={chart:{id:"attack-chart"},xaxis:{categories:e}}}return t},castSeries:function(){let t=[{name:"cast",data:[0]}],e=[];if(this.report&&this.report.attacks){for(var s=0;s<Object.keys(this.report.attacks["s"]).length;s++){let t=Object.keys(this.report.attacks["s"])[s],r=this.report.attacks["s"][t];e.push(r)}t=[{name:"hits",data:e}]}return t},statSeries:function(){let t=this.series;return this.info!=={}&&this.info.stats&&this.info.stats[0]&&(t=[{name:"series-1",data:[this.info.stats[0].value,this.info.stats[1].value,this.info.stats[2].value,this.info.stats[3].value,this.info.stats[4].value]}]),t},bodyClass:function(){return{dark_mode:this.darkMode}},sorted_tracks:function(){function t(t,e){return t.last_run<e.last_run?1:t.last_run>e.last_run?-1:0}let e=JSON.parse(JSON.stringify(this.track_report));return e.sort(t)},sorted_mkl:function(){let t=JSON.parse(JSON.stringify(this.mkl));return t.sort()},experience:function(){return this.report.exp+parseInt(this.info.total_exp)},exph:function(){var t=0;return this.report!=={}&&(t=60*this.report.expm),t},mobs_killed:function(){var t={};if(this.report.mobs_killed)for(var e=Object.keys(this.report.mobs_killed),s=e.length-1;s>=0;s--)t[e[s]]=this.report.mobs_killed[e[s]];return t},crit_to_hit:function(){let t=0;return this.report!=={}&this.report.total_phys_hits>0&&(t=Math.round(this.report.phys_crits/this.report.total_phys_hits*1e4)/100),t},crit_to_attack:function(){let t=0;return this.report!=={}&this.report.total_phys_attacks>0&&(t=Math.round(this.report.phys_crits/this.report.total_phys_attacks*1e4)/100),t},crit_to_cast:function(){let t=0;return this.report!=={}&this.report.spells_cast>0&&(t=Math.round(this.report.spell_crits/this.report.spells_cast*1e4)/100),t},crit_to_cast_hit:function(){let t=0;return this.report!=={}&this.report.spells_hit>0&&(t=Math.round(this.report.spell_crits/this.report.spells_hit*1e4)/100),t},effective_phys:function(){var t=0;return this.report!=={}&&(t=Math.round(this.report.phys_hit_rate/100*this.report.average_phys_damage*100)/100),t},effective_spell:function(){var t=0;return this.report!=={}&&(t=Math.round(this.report.spell_hit_rate/100*this.report.average_spell_damage*100)/100),t},total_kills:function(){var t=0;if(this.report.mobs_killed)for(var e=Object.keys(this.report.mobs_killed),s=e.length-1;s>=0;s--)t+=this.report.mobs_killed[e[s]];return t},kpm:function(){var t=Math.round(this.report.runtime);return 0==t?-1:Math.round(100*this.total_kills/t)/100},classname:function(){switch(this.info.class){case"Ass":return"Assassin";case"Bar":return"Barbarian";case"Cle":return"Cleric";case"Fig":return"Fighter";case"Brd":return"Bard";case"Mon":return"Monk";case"Mag":return"Mage";case"Pal":return"Paladin";case"Ran":return"Ranger";case"Thi":return"Thief";case"Dru":return"Druid";case"Alc":return"Alchemist";case"Dar":return"Anti-Paladin";default:return"Meow"}}}},Rt=s(89);const Ht=(0,Rt.Z)(Et,[["render",At]]);var It=Ht;const Kt=(0,r.ri)(It);Kt.use(i()),Kt.mount("#app")}},e={};function s(r){var a=e[r];if(void 0!==a)return a.exports;var i=e[r]={exports:{}};return t[r](i,i.exports,s),i.exports}s.m=t,function(){var t=[];s.O=function(e,r,a,i){if(!r){var n=1/0;for(p=0;p<t.length;p++){r=t[p][0],a=t[p][1],i=t[p][2];for(var o=!0,l=0;l<r.length;l++)(!1&i||n>=i)&&Object.keys(s.O).every((function(t){return s.O[t](r[l])}))?r.splice(l--,1):(o=!1,i<n&&(n=i));if(o){t.splice(p--,1);var c=a();void 0!==c&&(e=c)}}return e}i=i||0;for(var p=t.length;p>0&&t[p-1][2]>i;p--)t[p]=t[p-1];t[p]=[r,a,i]}}(),function(){s.n=function(t){var e=t&&t.__esModule?function(){return t["default"]}:function(){return t};return s.d(e,{a:e}),e}}(),function(){s.d=function(t,e){for(var r in e)s.o(e,r)&&!s.o(t,r)&&Object.defineProperty(t,r,{enumerable:!0,get:e[r]})}}(),function(){s.g=function(){if("object"===typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(t){if("object"===typeof window)return window}}()}(),function(){s.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)}}(),function(){s.r=function(t){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})}}(),function(){var t={143:0};s.O.j=function(e){return 0===t[e]};var e=function(e,r){var a,i,n=r[0],o=r[1],l=r[2],c=0;if(n.some((function(e){return 0!==t[e]}))){for(a in o)s.o(o,a)&&(s.m[a]=o[a]);if(l)var p=l(s)}for(e&&e(r);c<n.length;c++)i=n[c],s.o(t,i)&&t[i]&&t[i][0](),t[i]=0;return s.O(p)},r=self["webpackChunk"]=self["webpackChunk"]||[];r.forEach(e.bind(null,0)),r.push=e.bind(null,r.push.bind(r))}();var r=s.O(void 0,[998],(function(){return s(3354)}));r=s.O(r)})();
//# sourceMappingURL=app.1eac1ddb.js.map