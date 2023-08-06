"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[80736],{5435:(e,t,r)=>{r.a(e,(async e=>{r.d(t,{G:()=>a});var i=r(14516),n=r(54121),o=r(96191);n.Xp&&await n.Xp;const s=(0,i.Z)((e=>new Intl.RelativeTimeFormat(e.language,{numeric:"auto"}))),a=(e,t,r,i=!0)=>{const n=(0,o.W)(e,r);return i?s(t).format(n.value,n.unit):Intl.NumberFormat(t.language,{style:"unit",unit:n.unit,unitDisplay:"long"}).format(Math.abs(n.value))};e()}),1)},21780:(e,t,r)=>{r.d(t,{f:()=>i});const i=e=>e.charAt(0).toUpperCase()+e.slice(1)},96191:(e,t,r)=>{r.d(t,{W:()=>i});function i(e,t=Date.now(),r={}){const i={...n,...r||{}},o=(+e-+t)/1e3;if(Math.abs(o)<i.second)return{value:Math.round(o),unit:"second"};const s=o/60;if(Math.abs(s)<i.minute)return{value:Math.round(s),unit:"minute"};const a=o/3600;if(Math.abs(a)<i.hour)return{value:Math.round(a),unit:"hour"};const l=o/86400;if(Math.abs(l)<i.day)return{value:Math.round(l),unit:"day"};const d=o/604800;if(Math.abs(d)<i.week)return{value:Math.round(d),unit:"week"};const c=new Date(e),p=new Date(t),u=c.getFullYear()-p.getFullYear(),h=12*u+c.getMonth()-p.getMonth();return Math.round(Math.abs(h))<i.month?{value:Math.round(h),unit:"month"}:{value:Math.round(u),unit:"year"}}const n={second:45,minute:45,hour:22,day:5,week:4,month:11}},45339:(e,t,r)=>{r.d(t,{wC:()=>o,Ur:()=>a,F$:()=>l,iU:()=>d,eJ:()=>c,EB:()=>p,$X:()=>h});var i=r(97330),n=r(38346);const o={critical:1,error:2,warning:3},s=e=>e.sendMessagePromise({type:"repairs/list_issues"}),a=async(e,t,r)=>e.callWS({type:"repairs/ignore_issue",issue_id:t.issue_id,domain:t.domain,ignore:r}),l=(e,t,r)=>e.callApi("POST","repairs/issues/fix",{handler:t,issue_id:r}),d=(e,t)=>e.callApi("GET",`repairs/issues/fix/${t}`),c=(e,t,r)=>e.callApi("POST",`repairs/issues/fix/${t}`,r),p=(e,t)=>e.callApi("DELETE",`repairs/issues/fix/${t}`),u=(e,t)=>e.subscribeEvents((0,n.D)((()=>s(e).then((e=>t.setState(e,!0)))),500,!0),"repairs_issue_registry_updated"),h=(e,t)=>(0,i.B)("_repairsIssueRegistry",s,u,e,t)},52871:(e,t,r)=>{r.d(t,{w:()=>o});var i=r(47181);const n=()=>Promise.all([r.e(29563),r.e(24103),r.e(98985),r.e(59799),r.e(6294),r.e(88278),r.e(41985),r.e(85084),r.e(78874),r.e(45507),r.e(51644),r.e(68200),r.e(49842),r.e(1548),r.e(49075),r.e(5183),r.e(77576),r.e(29925),r.e(12545),r.e(26272),r.e(67681),r.e(4940),r.e(68101),r.e(15192)]).then(r.bind(r,93990)),o=(e,t,r)=>{(0,i.B)(e,"show-dialog",{dialogTag:"dialog-data-entry-flow",dialogImport:n,dialogParams:{...t,flowConfig:r,dialogParentElement:e}})}},80736:(e,t,r)=>{r.a(e,(async e=>{r(24103);var t=r(37500),i=r(33310),n=r(5435),o=r(21780),s=(r(9381),r(22098),r(73366),r(52039),r(5986)),a=(r(60010),r(11254)),l=r(60904),d=r(33807),c=e([n]);function p(){p=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!m(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var d=l.extras;if(d){for(var c=0;c<d.length;c++)this.addElementPlacement(d[c],t);r.push.apply(r,d)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return v(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?v(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=w(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:y(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=y(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function u(e){var t,r=w(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function h(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function m(e){return e.decorators&&e.decorators.length}function f(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function y(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function w(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function v(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}n=(c.then?await c:c)[0];!function(e,t,r,i){var n=p();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),r),a=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(f(o.descriptor)||f(n.descriptor)){if(m(o)||m(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(m(o)){if(m(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}h(o,n)}else t.push(o)}return t}(s.d.map(u)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,i.Mo)("ha-config-repairs")],(function(e,r){return{F:class extends r{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,i.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,i.Cb)({type:Boolean})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,i.Cb)({attribute:!1})],key:"repairsIssues",value:void 0},{kind:"field",decorators:[(0,i.Cb)({type:Number})],key:"total",value:void 0},{kind:"method",key:"render",value:function(){var e;if(null===(e=this.repairsIssues)||void 0===e||!e.length)return t.dy``;const r=this.repairsIssues;return t.dy`
      <div class="title">
        ${this.hass.localize("ui.panel.config.repairs.title",{count:this.total||this.repairsIssues.length})}
      </div>
      <mwc-list>
        ${r.map((e=>{var r;return t.dy`
            <ha-list-item
              twoline
              graphic="medium"
              .hasMeta=${!this.narrow}
              .issue=${e}
              class=${e.ignored?"ignored":""}
              @click=${this._openShowMoreDialog}
            >
              <img
                loading="lazy"
                src=${(0,a.X1)({domain:e.issue_domain||e.domain,type:"icon",useFallback:!0,darkOptimized:null===(r=this.hass.themes)||void 0===r?void 0:r.darkMode})}
                .title=${(0,s.Lh)(this.hass.localize,e.domain)}
                referrerpolicy="no-referrer"
                slot="graphic"
              />
              <span
                >${this.hass.localize(`component.${e.domain}.issues.${e.translation_key||e.issue_id}.title`,e.translation_placeholders||{})}</span
              >
              <span slot="secondary" class="secondary">
                ${"critical"===e.severity||"error"===e.severity?t.dy`<span class="error"
                      >${this.hass.localize(`ui.panel.config.repairs.${e.severity}`)}</span
                    >`:""}
                ${"critical"!==e.severity&&"error"!==e.severity||!e.created?"":" - "}
                ${e.created?(0,o.f)((0,n.G)(new Date(e.created),this.hass.locale)):""}
                ${e.ignored?` - ${this.hass.localize("ui.panel.config.repairs.dialog.ignored_in_version_short",{version:e.dismissed_version})}`:""}
              </span>
              ${this.narrow?"":t.dy`<ha-icon-next slot="meta"></ha-icon-next>`}
            </ha-list-item>
          `}))}
      </mwc-list>
    `}},{kind:"method",key:"_openShowMoreDialog",value:function(e){const t=e.currentTarget.issue;t.is_fixable?(0,l.w)(this,t):(0,d.W)(this,{issue:t})}},{kind:"field",static:!0,key:"styles",value:()=>t.iv`
    :host {
      --mdc-list-vertical-padding: 0;
    }
    .title {
      font-size: 16px;
      padding: 16px;
      padding-bottom: 0;
    }
    .ignored {
      opacity: var(--light-secondary-opacity);
    }
    ha-list-item {
      --mdc-list-item-graphic-size: 40px;
    }
    button.show-more {
      color: var(--primary-color);
      text-align: left;
      cursor: pointer;
      background: none;
      border-width: initial;
      border-style: none;
      border-color: initial;
      border-image: initial;
      padding: 16px;
      font: inherit;
    }
    button.show-more:focus {
      outline: none;
      text-decoration: underline;
    }
    ha-list-item {
      cursor: pointer;
      font-size: 16px;
    }
    .error {
      color: var(--error-color);
    }
  `}]}}),t.oi)}))},60904:(e,t,r)=>{r.d(t,{w:()=>a});var i=r(37500),n=r(5986),o=r(45339),s=r(52871);const a=(e,t,r)=>(0,s.w)(e,{startFlowHandler:t.domain,domain:t.domain,dialogClosedCallback:r},{loadDevicesAndAreas:!1,createFlow:async(e,r)=>{const[i]=await Promise.all([(0,o.F$)(e,r,t.issue_id),e.loadBackendTranslation("issues",t.domain)]);return i},fetchFlow:async(e,r)=>{const[i]=await Promise.all([(0,o.iU)(e,r),e.loadBackendTranslation("issues",t.domain)]);return i},handleFlowStep:o.eJ,deleteFlow:o.EB,renderAbortDescription(e,r){const n=e.localize(`component.${t.domain}.issues.abort.${r.reason}`,r.description_placeholders);return n?i.dy`
              <ha-markdown
                breaks
                allowsvg
                .content=${n}
              ></ha-markdown>
            `:""},renderShowFormStepHeader:(e,r)=>e.localize(`component.${t.domain}.issues.${t.translation_key||t.issue_id}.fix_flow.step.${r.step_id}.title`,r.description_placeholders)||e.localize("ui.dialogs.repair_flow.form.header"),renderShowFormStepDescription(e,r){const n=e.localize(`component.${t.domain}.issues.${t.translation_key||t.issue_id}.fix_flow.step.${r.step_id}.description`,r.description_placeholders);return n?i.dy`
              <ha-markdown
                allowsvg
                breaks
                .content=${n}
              ></ha-markdown>
            `:""},renderShowFormStepFieldLabel:(e,r,i)=>e.localize(`component.${t.domain}.issues.${t.translation_key||t.issue_id}.fix_flow.step.${r.step_id}.data.${i.name}`),renderShowFormStepFieldHelper(e,r,n){const o=e.localize(`component.${t.domain}.issues.${t.translation_key||t.issue_id}.fix_flow.step.${r.step_id}.data_description.${n.name}`,r.description_placeholders);return o?i.dy`<ha-markdown breaks .content=${o}></ha-markdown>`:""},renderShowFormStepFieldError:(e,r,i)=>e.localize(`component.${t.domain}.issues.${t.translation_key||t.issue_id}.fix_flow.error.${i}`,r.description_placeholders),renderExternalStepHeader:(e,t)=>"",renderExternalStepDescription:(e,t)=>"",renderCreateEntryDescription:(e,t)=>i.dy`
          <p>${e.localize("ui.dialogs.repair_flow.success.description")}</p>
        `,renderShowFormProgressHeader:(e,r)=>e.localize(`component.${t.domain}.issues.step.${t.translation_key||t.issue_id}.fix_flow.${r.step_id}.title`)||e.localize(`component.${t.domain}.title`),renderShowFormProgressDescription(e,r){const n=e.localize(`component.${t.domain}.issues.${t.translation_key||t.issue_id}.fix_flow.progress.${r.progress_action}`,r.description_placeholders);return n?i.dy`
              <ha-markdown
                allowsvg
                breaks
                .content=${n}
              ></ha-markdown>
            `:""},renderMenuHeader:(e,r)=>e.localize(`component.${t.domain}.issues.${t.translation_key||t.issue_id}.fix_flow.step.${r.step_id}.title`)||e.localize(`component.${t.domain}.title`),renderMenuDescription(e,r){const n=e.localize(`component.${t.domain}.issues.${t.translation_key||t.issue_id}.fix_flow.step.${r.step_id}.description`,r.description_placeholders);return n?i.dy`
              <ha-markdown
                allowsvg
                breaks
                .content=${n}
              ></ha-markdown>
            `:""},renderMenuOption:(e,r,i)=>e.localize(`component.${t.domain}.issues.${t.translation_key||t.issue_id}.fix_flow.step.${r.step_id}.menu_issues.${i}`,r.description_placeholders),renderLoadingDescription:(e,r)=>e.localize(`component.${t.domain}.issues.${t.translation_key||t.issue_id}.fix_flow.loading`)||("loading_flow"===r||"loading_step"===r?e.localize(`ui.dialogs.repair_flow.loading.${r}`,{integration:(0,n.Lh)(e.localize,t.domain)}):"")})},33807:(e,t,r)=>{r.d(t,{W:()=>o});var i=r(47181);const n=()=>Promise.all([r.e(85084),r.e(86603),r.e(29925),r.e(4940),r.e(14921)]).then(r.bind(r,14921)),o=(e,t)=>{(0,i.B)(e,"show-dialog",{dialogTag:"dialog-repairs-issue",dialogImport:n,dialogParams:t})}},11254:(e,t,r)=>{r.d(t,{X1:()=>i,RU:()=>n,u4:()=>o,zC:()=>s});const i=e=>e.domain.startsWith("ais_")?`https://ai-speaker.com/images/brands/${e.domain}/${e.type}.png`:`https://brands.home-assistant.io/${e.brand?"brands/":""}${e.useFallback?"_/":""}${e.domain}/${e.darkOptimized?"dark_":""}${e.type}.png`,n=e=>`https://brands.home-assistant.io/hardware/${e.category}/${e.darkOptimized?"dark_":""}${e.manufacturer}${e.model?`_${e.model}`:""}.png`,o=e=>e.split("/")[4],s=e=>e.startsWith("https://brands.home-assistant.io/")}}]);
//# sourceMappingURL=276633ab.js.map