"use strict";(self.webpackChunkpity=self.webpackChunkpity||[]).push([[331],{5966:function(T,v,t){var u=t(97685),s=t(1413),S=t(45987),I=t(21770),g=t(8232),V=t(55241),B=t(97435),R=t(67294),M=t(3607),h=t(85893),_=["fieldProps","proFieldProps"],K=["fieldProps","proFieldProps"],P="text",m=function(a){var n=a.fieldProps,l=a.proFieldProps,p=(0,S.Z)(a,_);return(0,h.jsx)(M.Z,(0,s.Z)({valueType:P,fieldProps:n,filedConfig:{valueType:P},proFieldProps:l},p))},y=function(a){var n=(0,I.Z)(a.open||!1,{value:a.open,onChange:a.onOpenChange}),l=(0,u.Z)(n,2),p=l[0],e=l[1];return(0,h.jsx)(g.Z.Item,{shouldUpdate:!0,noStyle:!0,children:function(F){var j,Z=F.getFieldValue(a.name||[]);return(0,h.jsx)(V.Z,(0,s.Z)((0,s.Z)({getPopupContainer:function(d){return d&&d.parentNode?d.parentNode:d},onOpenChange:function(d){return e(d)},content:(0,h.jsxs)("div",{style:{padding:"4px 0"},children:[(j=a.statusRender)===null||j===void 0?void 0:j.call(a,Z),a.strengthText?(0,h.jsx)("div",{style:{marginTop:10},children:(0,h.jsx)("span",{children:a.strengthText})}):null]}),overlayStyle:{width:240},placement:"rightTop"},a.popoverProps),{},{open:p,children:a.children}))}})},w=function(a){var n=a.fieldProps,l=a.proFieldProps,p=(0,S.Z)(a,K),e=(0,R.useState)(!1),C=(0,u.Z)(e,2),F=C[0],j=C[1];return n!=null&&n.statusRender&&p.name?(0,h.jsx)(y,{name:p.name,statusRender:n==null?void 0:n.statusRender,popoverProps:n==null?void 0:n.popoverProps,strengthText:n==null?void 0:n.strengthText,open:F,onOpenChange:j,children:(0,h.jsx)("div",{children:(0,h.jsx)(M.Z,(0,s.Z)({valueType:"password",fieldProps:(0,s.Z)((0,s.Z)({},(0,B.Z)(n,["statusRender","popoverProps","strengthText"])),{},{onBlur:function(D){var d;n==null||(d=n.onBlur)===null||d===void 0||d.call(n,D),j(!1)},onClick:function(D){var d;n==null||(d=n.onClick)===null||d===void 0||d.call(n,D),j(!0)}}),proFieldProps:l,filedConfig:{valueType:P}},p))})}):(0,h.jsx)(M.Z,(0,s.Z)({valueType:"password",fieldProps:n,proFieldProps:l,filedConfig:{valueType:P}},p))},O=m;O.Password=w,O.displayName="ProFormComponent",v.Z=O},952:function(T,v,t){var u=t(34994);v.ZP=u.A},88372:function(T,v,t){t.d(v,{f:function(){return K}});var u=t(4942),s=t(28459),S=t(93967),I=t.n(S),g=t(67294),V=t(76509),B=t(1413),R=t(98082),M=function(m){return(0,u.Z)({},m.componentCls,{width:"100%","&-wide":{maxWidth:1152,margin:"0 auto"}})};function h(P){return(0,R.Xj)("ProLayoutGridContent",function(m){var y=(0,B.Z)((0,B.Z)({},m),{},{componentCls:".".concat(P)});return[M(y)]})}var _=t(85893),K=function(m){var y=(0,g.useContext)(V.X),w=m.children,O=m.contentWidth,L=m.className,a=m.style,n=(0,g.useContext)(s.ZP.ConfigContext),l=n.getPrefixCls,p=m.prefixCls||l("pro"),e=O||y.contentWidth,C="".concat(p,"-grid-content"),F=h(C),j=F.wrapSSR,Z=F.hashId,D=e==="Fixed"&&y.layout==="top";return j((0,_.jsx)("div",{className:I()(C,Z,L,(0,u.Z)({},"".concat(C,"-wide"),D)),style:a,children:(0,_.jsx)("div",{className:"".concat(p,"-grid-content-children ").concat(Z).trim(),children:w})}))}},76509:function(T,v,t){t.d(v,{X:function(){return s}});var u=t(67294),s=(0,u.createContext)({})},58703:function(T,v,t){t.r(v),t.d(v,{default:function(){return te}});var u=t(97857),s=t.n(u),S=t(5574),I=t.n(S),g=t(67294),V=t(88372),B=t(50136),R=t(1413),M={icon:{tag:"svg",attrs:{viewBox:"64 64 896 896",focusable:"false"},children:[{tag:"path",attrs:{d:"M400 317.7h73.9V656c0 4.4 3.6 8 8 8h60c4.4 0 8-3.6 8-8V317.7H624c6.7 0 10.4-7.7 6.3-12.9L518.3 163a8 8 0 00-12.6 0l-112 141.7c-4.1 5.3-.4 13 6.3 13zM878 626h-60c-4.4 0-8 3.6-8 8v154H214V634c0-4.4-3.6-8-8-8h-60c-4.4 0-8 3.6-8 8v198c0 17.7 14.3 32 32 32h684c17.7 0 32-14.3 32-32V634c0-4.4-3.6-8-8-8z"}}]},name:"upload",theme:"outlined"},h=M,_=t(84089),K=function(i,f){return g.createElement(_.Z,(0,R.Z)((0,R.Z)({},i),{},{ref:f,icon:h}))},P=g.forwardRef(K),m=P,y=t(66476),w=t(14726),O=t(8232),L=t(952),a=t(5966),n=t(90596),l={baseView:"baseView___CxZTz",left:"left___XO1C6",right:"right___Sf2Ie",avatar_title:"avatar_title___jh8rZ",avatar:"avatar___BfnYL",button_view:"button_view___YUvAZ",area_code:"area_code___ii6L7",phone_number:"phone_number___J1m_l"},p=t(19478),e=t(85893),C=function(i,f,o){o()},F=function(i){var f=i.avatar,o=i.dispatch;return(0,e.jsxs)(e.Fragment,{children:[(0,e.jsx)("div",{className:l.avatar_title,children:"\u5934\u50CF"}),(0,e.jsx)("div",{className:l.avatar,children:(0,e.jsx)("img",{src:f,alt:"avatar"})}),(0,e.jsx)(y.Z,{showUploadList:!1,customRequest:function(x){o({type:"user/avatar",payload:{file:x.file}})},fileList:[],children:(0,e.jsx)("div",{className:l.button_view,children:(0,e.jsxs)(w.ZP,{children:[(0,e.jsx)(m,{}),"\u66F4\u6362\u5934\u50CF"]})})})]})},j=function(i){var f=i.user,o=i.loading,r=i.dispatch,x=f.currentUser,A=O.Z.useForm(),z=I()(A,1),b=z[0],$=function(){return x?x.avatar?x.avatar:p.Z.AVATAR_URL:""},U=function(){var N=b.getFieldsValue();r({type:"user/updateUser",payload:s()(s()({},N),{},{id:x.id})}),r({type:"user/fetchCurrent"})};return(0,e.jsx)("div",{className:l.baseView,children:o?null:(0,e.jsxs)(e.Fragment,{children:[(0,e.jsx)("div",{className:l.left,children:(0,e.jsxs)(L.ZP,{form:b,layout:"vertical",onFinish:U,submitter:{resetButtonProps:{style:{display:"none"}},submitButtonProps:{children:"\u66F4\u65B0\u57FA\u672C\u4FE1\u606F"}},initialValues:s()(s()({},x),{},{phone:x==null?void 0:x.phone}),hideRequiredMark:!0,children:[(0,e.jsx)(a.Z,{width:"md",name:"name",label:"\u59D3\u540D",rules:[{required:!0,message:"\u8BF7\u8F93\u5165\u60A8\u7684\u59D3\u540D!"}]}),(0,e.jsx)(a.Z,{width:"md",name:"email",label:"\u90AE\u7BB1",rules:[{required:!0,message:"\u8BF7\u8F93\u5165\u60A8\u7684\u90AE\u7BB1!"}]}),(0,e.jsx)(a.Z,{width:"md",name:"phone",label:"\u8054\u7CFB\u7535\u8BDD",placeholder:"\u8F93\u5165\u7535\u8BDD\u540E\u53EF\u63A5\u6536\u9489\u9489/\u4F01\u4E1A\u5FAE\u4FE1\u901A\u77E5\u54E6",rules:[{required:!1,message:"\u8BF7\u8F93\u5165\u60A8\u7684\u8054\u7CFB\u7535\u8BDD!"},{validator:C}]})]})}),(0,e.jsx)("div",{className:l.right,children:(0,e.jsx)(F,{avatar:$(),dispatch:r})})]})})},Z=(0,n.connect)(function(E){var i=E.user;return{user:i}})(j),D=function(){var i=function(){return[{title:"\u7ED1\u5B9A\u6DD8\u5B9D",description:"\u5F53\u524D\u672A\u7ED1\u5B9A\u6DD8\u5B9D\u8D26\u53F7",actions:[_jsx("a",{children:"\u7ED1\u5B9A"},"Bind")],avatar:_jsx(TaobaoOutlined,{className:"taobao"})},{title:"\u7ED1\u5B9A\u652F\u4ED8\u5B9D",description:"\u5F53\u524D\u672A\u7ED1\u5B9A\u652F\u4ED8\u5B9D\u8D26\u53F7",actions:[_jsx("a",{children:"\u7ED1\u5B9A"},"Bind")],avatar:_jsx(AlipayOutlined,{className:"alipay"})},{title:"\u7ED1\u5B9A\u9489\u9489",description:"\u5F53\u524D\u672A\u7ED1\u5B9A\u9489\u9489\u8D26\u53F7",actions:[_jsx("a",{children:"\u7ED1\u5B9A"},"Bind")],avatar:_jsx(DingdingOutlined,{className:"dingding"})}]};return _jsx(Fragment,{children:_jsx(List,{itemLayout:"horizontal",dataSource:i(),renderItem:function(o){return _jsx(List.Item,{actions:o.actions,children:_jsx(List.Item.Meta,{avatar:o.avatar,title:o.title,description:o.description})})}})})},d=null,X=t(72269),W=t(2487),H=function(){var i=function(){var r=(0,e.jsx)(X.Z,{checkedChildren:"\u5F00",unCheckedChildren:"\u5173",defaultChecked:!0});return[{title:"\u8D26\u6237\u5BC6\u7801",description:"\u5176\u4ED6\u7528\u6237\u7684\u6D88\u606F\u5C06\u4EE5\u7AD9\u5185\u4FE1\u7684\u5F62\u5F0F\u901A\u77E5",actions:[r]},{title:"\u7CFB\u7EDF\u6D88\u606F",description:"\u7CFB\u7EDF\u6D88\u606F\u5C06\u4EE5\u7AD9\u5185\u4FE1\u7684\u5F62\u5F0F\u901A\u77E5",actions:[r]},{title:"\u5F85\u529E\u4EFB\u52A1",description:"\u5F85\u529E\u4EFB\u52A1\u5C06\u4EE5\u7AD9\u5185\u4FE1\u7684\u5F62\u5F0F\u901A\u77E5",actions:[r]}]},f=i();return(0,e.jsx)(g.Fragment,{children:(0,e.jsx)(W.Z,{itemLayout:"horizontal",dataSource:f,renderItem:function(r){return(0,e.jsx)(W.Z.Item,{actions:r.actions,children:(0,e.jsx)(W.Z.Item.Meta,{title:r.title,description:r.description})})}})})},Y=H,J={strong:(0,e.jsx)("span",{className:"strong",children:"\u5F3A"}),medium:(0,e.jsx)("span",{className:"medium",children:"\u4E2D"}),weak:(0,e.jsx)("span",{className:"weak",children:"\u5F31 Weak"})},Q=function(){var i=function(){return[{title:"\u8D26\u6237\u5BC6\u7801",description:(0,e.jsxs)(e.Fragment,{children:["\u5F53\u524D\u5BC6\u7801\u5F3A\u5EA6\uFF1A",J.strong]}),actions:[(0,e.jsx)("a",{children:"\u4FEE\u6539"},"Modify")]},{title:"\u5BC6\u4FDD\u624B\u673A",description:"\u5DF2\u7ED1\u5B9A\u624B\u673A\uFF1A138****8293",actions:[(0,e.jsx)("a",{children:"\u4FEE\u6539"},"Modify")]},{title:"\u5BC6\u4FDD\u95EE\u9898",description:"\u672A\u8BBE\u7F6E\u5BC6\u4FDD\u95EE\u9898\uFF0C\u5BC6\u4FDD\u95EE\u9898\u53EF\u6709\u6548\u4FDD\u62A4\u8D26\u6237\u5B89\u5168",actions:[(0,e.jsx)("a",{children:"\u8BBE\u7F6E"},"Set")]},{title:"\u5907\u7528\u90AE\u7BB1",description:"\u5DF2\u7ED1\u5B9A\u90AE\u7BB1\uFF1Aant***sign.com",actions:[(0,e.jsx)("a",{children:"\u4FEE\u6539"},"Modify")]},{title:"MFA \u8BBE\u5907",description:"\u672A\u7ED1\u5B9A MFA \u8BBE\u5907\uFF0C\u7ED1\u5B9A\u540E\uFF0C\u53EF\u4EE5\u8FDB\u884C\u4E8C\u6B21\u786E\u8BA4",actions:[(0,e.jsx)("a",{children:"\u7ED1\u5B9A"},"bind")]}]},f=i();return(0,e.jsx)(e.Fragment,{children:(0,e.jsx)(W.Z,{itemLayout:"horizontal",dataSource:f,renderItem:function(r){return(0,e.jsx)(W.Z.Item,{actions:r.actions,children:(0,e.jsx)(W.Z.Item.Meta,{title:r.title,description:r.description})})}})})},k=Q,G={main:"main___mGCWD",leftMenu:"leftMenu___OBKuo",right:"right___j0rZL",title:"title___NjH5F"},q=B.Z.Item,ee=function(){var i={base:"\u57FA\u672C\u8BBE\u7F6E",security:"\u5B89\u5168\u8BBE\u7F6E",notification:"\u65B0\u6D88\u606F\u901A\u77E5"},f=(0,g.useState)({mode:"inline",selectKey:"base"}),o=I()(f,2),r=o[0],x=o[1],A=(0,g.useRef)(),z=function(){requestAnimationFrame(function(){if(!!A.current){var c="inline",N=A.current.offsetWidth;A.current.offsetWidth<641&&N>400&&(c="horizontal"),window.innerWidth<768&&N>400&&(c="horizontal"),x(s()(s()({},r),{},{mode:c}))}})};(0,g.useLayoutEffect)(function(){return A.current&&(window.addEventListener("resize",z),z()),function(){window.removeEventListener("resize",z)}},[A.current]);var b=function(){return Object.keys(i).map(function(c){return(0,e.jsx)(q,{children:i[c]},c)})},$=function(){var c=r.selectKey;switch(c){case"base":return(0,e.jsx)(Z,{});case"security":return(0,e.jsx)(k,{});case"notification":return(0,e.jsx)(Y,{});default:return null}};return(0,e.jsx)(V.f,{children:(0,e.jsxs)("div",{className:G.main,ref:function(c){c&&(A.current=c)},children:[(0,e.jsx)("div",{className:G.leftMenu,children:(0,e.jsx)(B.Z,{mode:r.mode,selectedKeys:[r.selectKey],onClick:function(c){var N=c.key;x(s()(s()({},r),{},{selectKey:N}))},children:b()})}),(0,e.jsxs)("div",{className:G.right,children:[(0,e.jsx)("div",{className:G.title,children:i[r.selectKey]}),$()]})]})})},te=ee},15746:function(T,v,t){var u=t(21584);v.Z=u.Z},71230:function(T,v,t){var u=t(92820);v.Z=u.Z}}]);