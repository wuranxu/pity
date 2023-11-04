(self.webpackChunkpity=self.webpackChunkpity||[]).push([[3807],{41612:function(T,Z,e){T=e.nmd(T);var r=e(52677).default;ace.define("ace/theme/material-one-dark",["require","exports","module","ace/lib/dom"],function(v,E,j){E.isDark=!1,E.cssClass="ace-material-one-dark",E.cssText=`
.ace-material-one-dark .ace_gutter {
  background: #272B33;
  color: rgb(103,111,122)
}

.ace-material-one-dark .ace_print-margin {
  // width: 1px;
  background: #e8e8e8
}

.ace-material-one-dark {
  background-color: #272B33;
  color: #A6B2C0
}

.ace-material-one-dark .ace_cursor {
  color: #528BFF
}

.ace-material-one-dark .ace_marker-layer .ace_selection {
  background: #3D4350
}

.ace-material-one-dark.ace_multiselect .ace_selection.ace_start {
  box-shadow: 0 0 3px 0px #272B33;
  border-radius: 2px
}

.ace-material-one-dark .ace_marker-layer .ace_step {
  background: rgb(198, 219, 174)
}

.ace-material-one-dark .ace_marker-layer .ace_bracket {
  margin: -1px 0 0 -1px;
  border: 1px solid #747369
}

.ace-material-one-dark .ace_marker-layer .ace_active-line {
  background: #2B313A
}

.ace-material-one-dark .ace_gutter-active-line {
  background-color: #2B313A
}

.ace-material-one-dark .ace_marker-layer .ace_selected-word {
  border: 1px solid #3D4350
}

.ace-material-one-dark .ace_fold {
  background-color: #61AEEF;
  border-color: #A6B2C0
}

.ace-material-one-dark .ace_keyword {
  color: #C679DD
}

.ace-material-one-dark .ace_keyword.ace_operator {
  color: #A6B2C0
}

.ace-material-one-dark .ace_keyword.ace_other.ace_unit {
  color: #D2945D
}

.ace-material-one-dark .ace_constant {
  color: #D2945D
}

.ace-material-one-dark .ace_constant.ace_numeric {
  color: #D2945D
}

.ace-material-one-dark .ace_constant.ace_character.ace_escape {
  color: #57B6C2
}

.ace-material-one-dark .ace_support.ace_function {
  color: #57B6C2
}

.ace-material-one-dark .ace_support.ace_class {
  color: #E5C17C
}

.ace-material-one-dark .ace_storage {
  color: #C679DD
}

.ace-material-one-dark .ace_invalid.ace_illegal {
  color: #272B33;
  background-color: #f2777a
}

.ace-material-one-dark .ace_invalid.ace_deprecated {
  color: #272B33;
  background-color: #d27b53
}

.ace-material-one-dark .ace_string {
  color: #90C378
}

.ace-material-one-dark .ace_string.ace_regexp {
  color: #57B6C2
}

.ace-material-one-dark .ace_comment {
  font-style: italic;
  color: #59626F
}

.ace-material-one-dark .ace_variable {
  color: #DF6A73
}

.ace-material-one-dark .ace_meta.ace_selector {
  color: #C679DD
}

.ace-material-one-dark .ace_entity.ace_other.ace_attribute-name {
  color: #D2945D
}

.ace-material-one-dark .ace_entity.ace_name.ace_function {
  color: #61AEEF
}

.ace-material-one-dark .ace_entity.ace_name.ace_tag {
  color: #DF6A73
}

.ace-material-one-dark .ace_markup.ace_list {
  color: #DF6A73
}
`;var I=v("ace/lib/dom");I.importCssString(E.cssText,E.cssClass)}),function(){ace.require(["ace/theme/ace-material-one-dark"],function(v){r(T)=="object"&&r(Z)=="object"&&T&&(T.exports=v)})}()},26194:function(T,Z,e){"use strict";e.d(Z,{Z:function(){return le}});var r=e(12444),v=e.n(r),E=e(72004),j=e.n(E),I=e(31996),O=e.n(I),m=e(26037),D=e.n(m),s=e(67294),L=e(53239),b=e.n(L),k=e(74981),c=e(82679),P=e.n(c),o=e(5619),R=e.n(o),se=e(41612),w=e.n(se),_=e(90252),ye=e.n(_),Y=e(85893),le=function(ie){O()(F,ie);var ce=D()(F);function F(){return v()(this,F),ce.apply(this,arguments)}return j()(F,[{key:"componentDidMount",value:function(){var t=this;this.props.setEditor(this.refs),(0,c.addCompleter)({getCompletions:function(z,ee,V,ne,n){n(null,(t.props.tables||[]).map(function(J){return{name:J,value:J}}))}})}},{key:"render",value:function(){var t=this.props,q=t.value,z=t.onChange,ee=t.height,V=t.readOnly,ne=t.theme;return(0,Y.jsx)(k.ZP,{ref:"aceEditor",mode:"json",theme:ne||"material-one-dark",fontSize:14,showGutter:!0,showPrintMargin:!1,onChange:z,value:q,wrapEnabled:!0,highlightActiveLine:!0,enableSnippets:!0,style:{width:"100%",height:ee||300},setOptions:{readOnly:V||!1,enableBasicAutocompletion:!0,enableLiveAutocompletion:!0,enableSnippets:!0,showLineNumbers:!0,tabSize:4,useWorker:!0}})}}]),F}(s.Component)},37594:function(T,Z,e){"use strict";e.d(Z,{B:function(){return E}});var r=e(91321),v="//at.alicdn.com/t/font_915840_2b8lahxt5xv.js",E=(0,r.Z)({scriptUrl:v})},56262:function(T,Z,e){"use strict";e.d(Z,{Z:function(){return J}});var r=e(67294),v=e(34041),E=e(96365),j=e(71230),I=e(15746),O=e(15009),m=e.n(O),D=e(19632),s=e.n(D),L=e(99289),b=e.n(L),k=e(5574),c=e.n(k),P=e(97857),o=e.n(P),R=e(13769),se=e.n(R),w=e(52445),_=e(45360),ye=e(86738),Y=e(96021),le=e(96074),ie=e(71577),ce=e(64997),F=e(51042),ue=e(19478),t=e(85893),q=["editing","dataIndex","title","type","setType","record","index","key","children"],z=v.Z.Option,ee=function(u){var K=u.editing,U=u.dataIndex,$=u.title,te=u.type,B=u.setType,h=u.record,de=u.index,ve=u.key,H=u.children,X=se()(u,q);return(0,t.jsx)("td",o()(o()({},X),{},{children:K?(0,t.jsx)(w.Z.Item,{name:U,style:{margin:0},initialValue:h.dataIndex,rules:[{required:!0,message:"Please Input ".concat($,"!")}],children:(0,t.jsx)(E.Z,{placeholder:"please input ".concat($)})}):H}))},V=function(u){var K=u.data,U=u.setData,$=u.ossFileList,te=w.Z.useForm(),B=c()(te,1),h=B[0],de=(0,r.useState)(""),ve=c()(de,2),H=ve[0],X=ve[1],pe=(0,r.useState)("FILE"),N=c()(pe,2),G=N[0],me=N[1],Ee=(0,r.useState)(null),je=c()(Ee,2),Q=je[0],Ce=je[1],he=function(f){return f.key===H},De=function(f){h.setFieldsValue(o()({},f)),X(f.key)},Se=function(){X("")},Oe=function(){var C=b()(m()().mark(function f(l){var y,g,re,oe,be;return m()().wrap(function(p){for(;;)switch(p.prev=p.next){case 0:return p.prev=0,p.next=3,h.validateFields();case 3:if(y=p.sent,!(G==="FILE"&&!Q)){p.next=7;break}return _.ZP.info("\u8BF7\u9009\u62E9\u6587\u4EF6"),p.abrupt("return");case 7:if(g=s()(K),re=g.findIndex(function(ge){return l===ge.key}),!(re>-1)){p.next=20;break}if(oe=g[re],be=g.findIndex(function(ge){return y.key===ge.key}),!(be>-1)){p.next=15;break}return _.ZP.info("\u8BE5key\u5DF2\u5B58\u5728"),p.abrupt("return");case 15:g.splice(re,1,o()(o()(o()({},oe),y),{},{type:G,value:Q})),U(g),X(""),p.next=23;break;case 20:g.push(o()(o()({},y),{},{type:G,value:Q})),U(g),X("");case 23:p.next=28;break;case 25:p.prev=25,p.t0=p.catch(0),console.log("Validate Failed:",p.t0);case 28:case"end":return p.stop()}},f,null,[[0,25]])}));return function(l){return C.apply(this,arguments)}}(),Te=function(f){var l=s()(K);l.splice(l.findIndex(function(y){return f===y.key}),1),U(l)},fe=[{title:"KEY",dataIndex:"key",width:"30%",editable:!0},{title:"TYPE",dataIndex:"type",type:"select",width:"10%",render:function(f,l){return l.key===H?(0,t.jsxs)(v.Z,{style:{width:"100%"},value:G,onChange:function(g){me(g)},children:[(0,t.jsx)(z,{value:"FILE",children:"FILE"}),(0,t.jsx)(z,{value:"TEXT",children:"TEXT"})]}):l.type}},{title:"VALUE",dataIndex:"value",width:"40%",render:function(f,l){return l.key===H?G==="FILE"?(0,t.jsx)(v.Z,{style:{width:"100%"},placeholder:"please select oss file",showSearch:!0,value:Q,onChange:function(g){return Ce(g)},children:$.map(function(y){return(0,t.jsx)(z,{value:y.file_path,children:y.file_path},y.file_path)})}):(0,t.jsx)(E.Z,{placeholder:"please input VALUE",value:Q,onChange:function(g){Ce(g.target.value)}}):G==="FILE"?(0,t.jsx)("a",{href:"".concat(ue.Z.URL,"/oss/download?filepath=").concat(l.value),children:l.value}):l.value}},{title:"OPERATION",dataIndex:"operation",render:function(f,l){var y=he(l);return y?(0,t.jsxs)("span",{children:[(0,t.jsx)("a",{onClick:function(){return Oe(l.key)},style:{marginRight:8},children:"Save"}),(0,t.jsx)(ye.Z,{title:"Sure to cancel?",onConfirm:Se,children:(0,t.jsx)("a",{children:"Cancel"})})]}):(0,t.jsxs)(t.Fragment,{children:[(0,t.jsx)(Y.Z.Link,{disabled:H!=="",onClick:function(){return De(l)},children:"Edit"}),(0,t.jsx)(le.Z,{type:"vertical"}),(0,t.jsx)(Y.Z.Link,{disabled:H!=="",onClick:function(){return Te(l.key)},children:"Remove"})]})}}],ae=function(){var f=[].concat(s()(K),[{key:"",type:"TEXT",value:null}]);U(f),me("FILE")},Ze=fe.map(function(C){return C.editable?o()(o()({},C),{},{onCell:function(l,y){return{record:l,index:y,type:G,setType:me,dataIndex:C.dataIndex,title:C.title,editing:he(l)}}}):C});return(0,t.jsxs)(t.Fragment,{children:[(0,t.jsx)(j.Z,{style:{marginBottom:12},children:(0,t.jsx)(I.Z,{span:6,children:(0,t.jsx)(ie.ZP,{type:"primary",onClick:ae,icon:(0,t.jsx)(F.Z,{}),children:"Add"})})}),(0,t.jsx)(w.Z,{form:h,component:!1,children:(0,t.jsx)(ce.Z,{components:{body:{cell:ee}},dataSource:K,columns:Ze,rowClassName:"editable-row",pagination:{onChange:Se}})})]})},ne=V,n=v.Z.Option,J=function(M){var u=M.ossFileList,K=M.dataSource,U=M.setDataSource,$=[{title:"KEY",dataIndex:"key",render:function(){return(0,t.jsx)(E.Z,{})}},{title:"VALUE",dataIndex:"value",render:function(){return(0,t.jsx)(v.Z,{children:u.map(function(B){return(0,t.jsx)(n,{value:B.key,children:B.key},B.key)})})}}];return(0,t.jsx)(j.Z,{gutter:8,style:{marginTop:16},children:(0,t.jsx)(I.Z,{span:24,children:(0,t.jsx)(ne,{bordered:!0,columns:$,data:K,setData:U,ossFileList:u})})})}},53677:function(T,Z,e){"use strict";var r=e(67294),v=e(13433),E=e(85893);Z.Z=function(j){var I=j.columns,O=j.dataSource,m=j.title,D=j.setDataSource,s=j.editableKeys,L=j.setEditableRowKeys,b=j.extra;return(0,r.useEffect)(function(){L(O.map(function(k){return k.id}))},[O]),(0,E.jsx)(v.Z,{headerTitle:m,columns:I,rowKey:"id",value:O,onChange:D,recordCreatorProps:{newRecordType:"dataSource",record:function(){return{id:Date.now()}}},editable:{type:"multiple",editableKeys:s,actionRender:function(c,P,o){return[o.delete]},onValuesChange:function(c,P){b&&b(P),D(P)},onChange:L}})}},26969:function(T,Z,e){"use strict";e.r(Z),e.d(Z,{default:function(){return te}});var r=e(67294),v=e(52677),E=e.n(v),j=e(15009),I=e.n(j),O=e(99289),m=e.n(O),D=e(5574),s=e.n(D),L=e(34041),b=e(48055),k=e(26855),c=e(75308),P=e(71230),o=e(15746),R=e(4393),se=e(96365),w=e(71577),_=e(55742),ye=e(85418),Y=e(64997),le=e(65987),ie=e(31484),ce=e(34804),F=e(53677),ue=e(12414),t=e(90596),q=e(10981),z=e(56262),ee=e(37594),V=e(26194),ne=e(11609),n=e(85893),J=L.Z.Option,M=b.Z.TabPane,u={200:{color:"#67C23A",text:"OK"},401:{color:"#F56C6C",text:"unauthorized"},400:{color:"#F56C6C",text:"Bad Request"}},K=function(h){return h&&h.response?(0,n.jsx)("div",{style:{marginRight:16},children:(0,n.jsxs)("span",{children:["Status:",(0,n.jsxs)("span",{style:{color:u[h.status_code]?u[h.status_code].color:"#F56C6C",marginLeft:8,marginRight:8},children:[h.status_code," ",u[h.status_code]?u[h.status_code].text:""]}),(0,n.jsxs)("span",{style:{marginLeft:8,marginRight:8},children:["Time: ",(0,n.jsx)("span",{style:{color:"#67C23A"},children:h.cost})]})]})}):null},U=function(h){var de=h.loading,ve=h.gconfig,H=h.dispatch,X=(0,r.useState)(0),pe=s()(X,2),N=pe[0],G=pe[1],me=(0,r.useState)("JSON"),Ee=s()(me,2),je=Ee[0],Q=Ee[1],Ce=(0,r.useState)("GET"),he=s()(Ce,2),De=he[0],Se=he[1],Oe=(0,r.useState)([]),Te=s()(Oe,2),fe=Te[0],ae=Te[1],Ze=(0,r.useState)([]),C=s()(Ze,2),f=C[0],l=C[1],y=(0,r.useState)(function(){return fe.map(function(d){return d.id})}),g=s()(y,2),re=g[0],oe=g[1],be=(0,r.useState)(function(){return f.map(function(d){return d.id})}),Ie=s()(be,2),p=Ie[0],ge=Ie[1],Ye=(0,r.useState)(null),ke=s()(Ye,2),Le=ke[0],Ve=ke[1],Qe=(0,r.useState)(!1),_e=s()(Qe,2),we=_e[0],Me=_e[1],qe=(0,r.useState)({}),Ae=s()(qe,2),A=Ae[0],en=Ae[1],nn=(0,r.useState)([]),Re=s()(nn,2),Be=Re[0],tn=Re[1],an=(0,r.useState)(null),Fe=s()(an,2),yn=Fe[0],Ke=Fe[1],rn=ve.ossFileList,on=(0,r.useState)(""),Ue=s()(on,2),Pe=Ue[0],We=Ue[1],sn=(0,n.jsxs)(L.Z,{value:De,onChange:function(a){return Se(a)},style:{width:120,fontSize:16,textAlign:"left"},children:[(0,n.jsx)(J,{value:"GET",children:"GET"},"GET"),(0,n.jsx)(J,{value:"POST",children:"POST"},"POST"),(0,n.jsx)(J,{value:"PUT",children:"PUT"},"PUT"),(0,n.jsx)(J,{value:"DELETE",children:"DELETE"},"DELETE")]}),Je=[{title:"KEY",dataIndex:"key",key:"key"},{title:"VALUE",dataIndex:"value",key:"value"}],He=function(a){if(A[a]===null||A[a]===void 0||A[a]==="{}")return[];var i=JSON.parse(A[a]);return Object.keys(i).map(function(x){return{key:x,value:i[x]}})},Ne=function(a){var i=Pe.split("?")[0];a.forEach(function(x,W){x.key&&(W===0?i="".concat(i,"?").concat(x.key,"=").concat(x.value||""):i="".concat(i,"&").concat(x.key,"=").concat(x.value||""))}),We(i)},ln=function(a){var i=a.split("?");if(i.length<2)ae([]);else{var x=i[1].split("&"),W=[],S=[];x.forEach(function(hn,ze){var fn=hn.split("="),$e=s()(fn,2),gn=$e[0],xn=$e[1],Xe=Date.now();S.push(Xe+ze+10),W.push({key:gn,value:xn,id:Xe+ze+10,description:""})}),ae(W),oe(S)}},xe=function(a){Q(a)},cn=function(){var a={};return f.forEach(function(i){i.key!==""&&(a[i.key]=i.value)}),a},un=function(){var d=m()(I()().mark(function a(){var i,x;return I()().wrap(function(S){for(;;)switch(S.prev=S.next){case 0:if(Pe!==""){S.next=3;break}return k.Z.error({message:"\u8BF7\u6C42Url\u4E0D\u80FD\u4E3A\u7A7A"}),S.abrupt("return");case 3:return Me(!0),i={method:De,url:Pe,body:N===2?JSON.stringify(Be):Le,body_type:N,headers:cn()},N===0&&(i.body=null),S.next=8,(0,ue.c3)(i);case 8:x=S.sent,Me(!1),q.Z.response(x,!0)&&en(x.data);case 11:case"end":return S.stop()}},a)}));return function(){return d.apply(this,arguments)}}(),dn=function(a,i){if(a==="params"){var x=fe.filter(function(S){return S.id!==i});ae(x),Ne(x)}else{var W=f.filter(function(S){return S.id!==i});l(W)}},vn=(0,n.jsxs)(c.Z,{children:[(0,n.jsx)(c.Z.Item,{children:(0,n.jsx)("a",{onClick:function(){xe("Text")},children:"Text"})},"Text"),(0,n.jsx)(c.Z.Item,{children:(0,n.jsx)("a",{onClick:function(){xe("JavaScript")},children:"JavaScript"})},"JavaScript"),(0,n.jsx)(c.Z.Item,{children:(0,n.jsx)("a",{onClick:function(){xe("JSON")},children:"JSON"})},"JSON"),(0,n.jsx)(c.Z.Item,{children:(0,n.jsx)("a",{onClick:function(){xe("HTML")},children:"HTML"})},"HTML"),(0,n.jsx)(c.Z.Item,{children:(0,n.jsx)("a",{onClick:function(){xe("XML")},children:"XML"})},"XML")]}),Ge=function(a){return[{title:"KEY",key:"key",dataIndex:"key"},{title:"VALUE",key:"value",dataIndex:"value"},{title:"DESCRIPTION",key:"description",dataIndex:"description"},{title:"\u64CD\u4F5C",valueType:"option",render:function(x,W){return(0,n.jsxs)(n.Fragment,{children:[(0,n.jsx)(le.Z,{style:{cursor:"pointer"},onClick:function(){oe([W.id])}}),(0,n.jsx)(ie.Z,{style:{cursor:"pointer",marginLeft:8},onClick:function(){dn(a,W.id)},twoToneColor:"#eb2f96"})]})}}]},mn=function(a){return a===0?(0,n.jsx)("div",{style:{height:"20vh",lineHeight:"20vh",textAlign:"center"},children:"This request does not have a body"}):a===2?(0,n.jsx)(z.Z,{ossFileList:rn,dataSource:Be,setDataSource:tn}):(0,n.jsx)(P.Z,{style:{marginTop:12},children:(0,n.jsx)(o.Z,{span:24,children:(0,n.jsx)(R.Z,{bodyStyle:{padding:0},children:(0,n.jsx)(V.Z,{value:Le,onChange:function(x){return Ve(x)},height:"20vh",setEditor:Ke})})})})};return(0,n.jsx)(ne._z,{title:"\u5728\u7EBFHTTP\u6D4B\u8BD5\u5DE5\u5177",breadcrumb:null,children:(0,n.jsxs)(R.Z,{children:[(0,n.jsxs)(P.Z,{gutter:[8,8],children:[(0,n.jsx)(o.Z,{span:18,children:(0,n.jsx)(se.Z,{size:"large",value:Pe,addonBefore:sn,placeholder:"\u8BF7\u8F93\u5165\u8981\u8BF7\u6C42\u7684url",onChange:function(a){We(a.target.value),ln(a.target.value)}})}),(0,n.jsx)(o.Z,{span:6,children:(0,n.jsxs)(w.ZP,{onClick:un,loading:we,type:"primary",size:"large",style:{marginRight:16,float:"right"},children:[(0,n.jsx)(ee.B,{type:"icon-fasong1"}),"Send"," "]})})]}),(0,n.jsx)(P.Z,{style:{marginTop:8},children:(0,n.jsxs)(b.Z,{defaultActiveKey:"1",style:{width:"100%"},children:[(0,n.jsx)(M,{tab:"Params",children:(0,n.jsx)(F.Z,{columns:Ge("params"),title:"Query Params",dataSource:fe,setDataSource:ae,extra:Ne,editableKeys:re,setEditableRowKeys:oe})},"1"),(0,n.jsx)(M,{tab:"Headers",children:(0,n.jsx)(F.Z,{columns:Ge("headers"),title:"Headers",dataSource:f,setDataSource:l,editableKeys:p,setEditableRowKeys:ge})},"2"),(0,n.jsxs)(M,{tab:"Body",children:[(0,n.jsxs)(P.Z,{children:[(0,n.jsxs)(_.ZP.Group,{defaultValue:0,value:N,onChange:function(a){G(a.target.value),a.target.value===2&&H({type:"gconfig/listOssFile"})},children:[(0,n.jsx)(_.ZP,{value:0,children:"none"}),(0,n.jsx)(_.ZP,{value:2,children:"form-data"}),(0,n.jsx)(_.ZP,{value:3,children:"x-www-form-urlencoded"}),(0,n.jsx)(_.ZP,{value:1,children:"raw"}),(0,n.jsx)(_.ZP,{value:4,children:"binary"}),(0,n.jsx)(_.ZP,{value:5,children:"GraphQL"})]}),N===1?(0,n.jsx)(ye.Z,{style:{marginLeft:8},overlay:vn,trigger:["click"],children:(0,n.jsxs)("a",{onClick:function(a){return a.preventDefault()},children:[je," ",(0,n.jsx)(ce.Z,{})]})}):null]}),mn(N)]},"3")]})}),(0,n.jsx)(P.Z,{gutter:[8,8],children:Object.keys(A).length===0?null:(0,n.jsxs)(b.Z,{style:{width:"100%"},tabBarExtraContent:K(A),children:[(0,n.jsx)(M,{tab:"Body",children:(0,n.jsx)(V.Z,{readOnly:!0,setEditor:Ke,language:A.response&&A.response_headers.indexOf("json")>-1?"json":"text",value:A.response&&E()(A.response)==="object"?JSON.stringify(A.response,null,2):A.response||"",height:"30vh"})},"1"),(0,n.jsx)(M,{tab:"Cookie",children:(0,n.jsx)(Y.Z,{columns:Je,dataSource:He("cookies"),size:"small",pagination:!1})},"2"),(0,n.jsx)(M,{tab:"Headers",children:(0,n.jsx)(Y.Z,{columns:Je,dataSource:He("response_headers"),size:"small",pagination:!1})},"3")]})})]})})},$=(0,t.connect)(function(B){var h=B.loading,de=B.gconfig;return{loading:h,gconfig:de}})(U),te=function(){return(0,n.jsx)($,{})}},5619:function(T,Z,e){T=e.nmd(T),ace.define("ace/ext/spellcheck",["require","exports","module","ace/lib/event","ace/editor","ace/config"],function(r,v,E){"use strict";var j=r("../lib/event");v.contextMenuHandler=function(O){var m=O.target,D=m.textInput.getElement();if(!!m.selection.isEmpty()){var s=m.getCursorPosition(),L=m.session.getWordRange(s.row,s.column),b=m.session.getTextRange(L);if(m.session.tokenRe.lastIndex=0,!!m.session.tokenRe.test(b)){var k="",c=b+" "+k;D.value=c,D.setSelectionRange(b.length,b.length+1),D.setSelectionRange(0,0),D.setSelectionRange(0,b.length);var P=!1;j.addListener(D,"keydown",function o(){j.removeListener(D,"keydown",o),P=!0}),m.textInput.setInputHandler(function(o){if(o==c)return"";if(o.lastIndexOf(c,0)===0)return o.slice(c.length);if(o.substr(D.selectionEnd)==c)return o.slice(0,-c.length);if(o.slice(-2)==k){var R=o.slice(0,-2);if(R.slice(-1)==" ")return P?R.substring(0,D.selectionEnd):(R=R.slice(0,-1),m.session.replace(L,R),"")}return o})}}};var I=r("../editor").Editor;r("../config").defineOptions(I.prototype,"editor",{spellcheck:{set:function(O){var m=this.textInput.getElement();m.spellcheck=!!O,O?this.on("nativecontextmenu",v.contextMenuHandler):this.removeListener("nativecontextmenu",v.contextMenuHandler)},value:!0}})}),function(){ace.require(["ace/ext/spellcheck"],function(r){T&&(T.exports=r)})}()}}]);
