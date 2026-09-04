from pathlib import Path

W, H = 350, 220

def esc(s):
    return str(s).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def main():
    lines = [
        ('OS', 'India / Windows + WSL'),
        ('STACK', 'React / Node / Express'),
        ('DATA', 'MongoDB / REST APIs'),
        ('BUILD', 'MERN + TypeScript'),
        ('SHIP', 'CRDT collaboration tools'),
        ('FOCUS', 'DSA / Full-Stack'),
        ('SOCIAL', 'linkedin.com/in/nikhil-bhatt-485046295'),
    ]
    text=''.join(f'<text x="24" y="{55+i*20}" fill="#8b949e" font-family="monospace" font-size="11"><tspan fill="#39d353">{k:<7}</tspan> {esc(v)}</text>' for i,(k,v) in enumerate(lines))
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<rect width="100%" height="100%" rx="14" fill="#0d1117" stroke="#30363d"/>
<circle cx="18" cy="15" r="4" fill="#ff5f56"/><circle cx="32" cy="15" r="4" fill="#ffbd2e"/><circle cx="46" cy="15" r="4" fill="#27c93f"/>
<text x="64" y="19" fill="#8b949e" font-family="monospace" font-size="10">nikhil@dev:~</text>
<text x="24" y="38" fill="#39d353" font-family="monospace" font-size="11">$ neofetch --profile</text>
{text}
<text x="24" y="203" fill="#39d353" font-family="monospace" font-size="11">nikhil@dev:~$ <animate attributeName="opacity" values="0;0;1" keyTimes="0;0.2;1" begin="0.01s" dur="0.35s" fill="freeze"/></text>
<rect x="132" y="193" width="7" height="13" fill="#39d353"><animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></rect>
</svg>'''
    Path('assets').mkdir(exist_ok=True)
    Path('assets/info-card.svg').write_text(svg,encoding='utf-8')

if __name__=='__main__': main()
