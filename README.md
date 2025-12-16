# N3rdL0rd's RHPS Audience Partici... ...pation Script

This repository contains the source code and the master script file for *N3rdL0rd's Audience Partici... ...pation Script* for the *Rocky Horror Picture Show*.

It uses some relatively simple Jinja2 to convert a custom plain-text markup format (`.rhps`) into a rich, responsive, and printable HTML script complete with color-coded callbacks, audience instructions, and cast cues.

## Usage

You need Python 3 installed, preferably with `uv`:

```bash
uv run build.py
```

### Generating the Script

1. Edit `script.rhps` to add your favorite callbacks.
2. Run the build script:

    ```bash
    python build.py
    ```

3. Open `index.html` in your browser to view the result.

---

## How to Contribute Callbacks

We want **YOUR** yells! Rocky is a living, breathing tradition, and callbacks vary by region, theater, and time period.

1. Fork this repository
2. Edit `script.rhps` to add your line
3. Submit a PR!

Please keep formatting clean and ensure your callback is placed exactly where it should be shouted in the movie.

---

## The `rhps` Markup Format

The builder uses a specific syntax to keep the script readable while allowing for formatting of callbacks.

### 1. Scenes

Start a new scene with a hash `#`.

```text
# Dammit, Janet
```

### 2. Dialogue

Format dialogue as `Character Name: Line`.
You can use multiple lines by indenting the subsequent lines.

```text
Brad: Hey, Janet.
    I've got something to say.
```

### 3. Basic Callbacks `< >`

Callbacks are enclosed in angle brackets. They appear in **Yellow**.

```text
Brad: <What do horses eat?> Hey, Janet.
```

### 4. Split Callbacks (Call / Answer) `< / >`

Use a forward slash `/` to split a callback between two groups or a Q&A format.

* Left side: **Green**
* Right side: **Pink**

```text
<Oh my god, you killed Kenya! / You bastard!>
```

### 5. Overlapping Callbacks `{ }< >`

If a callback is shouted *over* a specific line of dialogue (interruption), wrap the movie dialogue in `{}` immediately followed by the callback in `<>`.

```text
Brad: I really love the {skillful way}<What a genius!> you beat the other girls.
```

### 6. Screen Events `[ ]`

Use square brackets for things happening on screen (sound effects, visual cues). These appear in blue.

```text
[Thunder crashes]
```

### 7. Crowd Instructions `(( ))`

Use double parentheses for instructions for the audience (prop usage, actions). These appear in a large purple block.

```text
(( Throw rice now! ))
```

### 8. Cast Actions `[[ ]]`

Use double square brackets for shadowcast acting instructions (screenfucks). These appear in a smaller red block.

```text
[[ Run up and point at the screen ]]
```

### 9. Stage Directions

Any line that is not indented and does not start with a character name is treated as a generic stage direction.

---

> It's not easy having a good time... even smiling makes my face ache.
