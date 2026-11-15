const API = "/api/v1";
const $ = s => document.querySelector(s);
const status = msg => $("#status").textContent = msg;
const dbPromise = new Promise((resolve,reject)=>{
  const req=indexedDB.open("cv-studio-local",1);
  req.onupgradeneeded=()=>req.result.createObjectStore("drafts");
  req.onsuccess=()=>resolve(req.result); req.onerror=()=>reject(req.error);
});
async function localSave(key,value){const db=await dbPromise;return new Promise((res,rej)=>{const tx=db.transaction("drafts","readwrite");tx.objectStore("drafts").put(value,key);tx.oncomplete=res;tx.onerror=()=>rej(tx.error);});}
async function localLoad(key){const db=await dbPromise;return new Promise((res,rej)=>{const r=db.transaction("drafts").objectStore("drafts").get(key);r.onsuccess=()=>res(r.result);r.onerror=()=>rej(r.error);});}
document.querySelectorAll(".tab").forEach(b=>b.addEventListener("click",()=>{
 document.querySelectorAll(".tab").forEach(x=>x.classList.toggle("active",x===b));
 document.querySelectorAll(".panel").forEach(x=>x.classList.toggle("hidden",x.id!==b.dataset.tab));
}));
function addEntry(container,kind){const div=document.createElement("div");div.className="entry";
 div.innerHTML=`<input placeholder="Intitulé" data-field="title"><input placeholder="Organisation / établissement" data-field="organization"><input placeholder="Dates" data-field="dates"><input placeholder="Description" data-field="description">`;
 $(container).append(div);
}
$("#addExperience").onclick=()=>addEntry("#experiences","experience");
$("#addEducation").onclick=()=>addEntry("#education","education");
function entries(selector){return [...document.querySelectorAll(selector+" .entry")].map(e=>Object.fromEntries([...e.querySelectorAll("input")].map(i=>[i.dataset.field,i.value])));}
function cvData(){const f=new FormData($("#cvForm"));return {full_name:f.get("full_name"),email:f.get("email"),phone:f.get("phone"),city:f.get("city"),title:f.get("title"),summary:f.get("summary"),skills:f.get("skills").split(",").map(x=>x.trim()).filter(Boolean),experience:entries("#experiences"),education:entries("#education")};}
function letterData(){const f=new FormData($("#letterForm"));return {full_name:f.get("full_name"),recipient:f.get("recipient"),company:f.get("company"),role:f.get("role"),paragraphs:f.get("paragraphs").split("\\n").map(x=>x.trim()).filter(Boolean)};}
async function restore(key,form,transform){const d=await localLoad(key);if(!d)return;Object.entries(d).forEach(([k,v])=>{const el=form.elements[k];if(el && typeof v==="string")el.value=v;});}
$("#saveCv").onclick=async()=>{await localSave("cv",cvData());status("CV enregistré localement sur cet appareil.");};
$("#saveLetter").onclick=async()=>{await localSave("letter",letterData());status("Lettre enregistrée localement sur cet appareil.");};
async function pdf(endpoint,data,filename){status("Génération du document…");try{
 const r=await fetch(`${API}${endpoint}`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(data)});
 if(!r.ok){const e=await r.json().catch(()=>({}));throw new Error(e.error||"Erreur API");}
 const blob=await r.blob();const url=URL.createObjectURL(blob);const a=document.createElement("a");a.href=url;a.download=filename;a.click();URL.revokeObjectURL(url);status("PDF généré. Le fichier a été téléchargé.");
 }catch(e){status(`Impossible de générer le PDF : ${e.message}`);}}
$("#cvForm").onsubmit=e=>{e.preventDefault();pdf("/documents/cv/pdf",cvData(),"mon-cv.pdf");};
$("#letterForm").onsubmit=e=>{e.preventDefault();pdf("/documents/letter/pdf",letterData(),"lettre-motivation.pdf");};
fetch("/health").then(r=>r.ok?$("#connection").textContent="API connectée":Promise.reject()).catch(()=>$("#connection").textContent="API indisponible");
restore("cv",$("#cvForm"));restore("letter",$("#letterForm"));
if("serviceWorker" in navigator) navigator.serviceWorker.register("/sw.js").catch(()=>{});
