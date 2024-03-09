# Soul of Waifu - Core
[**| RU |**](README.MD)

<img src="docs/cont/preview.jpg" href="https://twitter.com/onisarashi"></img>

Art by: https://twitter.com/onisarashi

### | Multi-module core for communicating with neural networks

**Soul of Waifu** - console client for communicating with neural networks.

**Soul of Waifu Core** - a core that implements communication with neural networks, making it possible to add them thanks to interface modules. Extending the capabilities of the core.

The core implements input -> output of text and its transformation as the chain passes through the interfaces implemented by the modules.

![logic](docs/cont/dialog_entity.png)

The multimodularity of the core is achieved through a system of addons.
Each addon implements a module according to the interface characteristics.

### | Basic equipment

In this repository you can download a version of Soul of Waifu with the CharacterAI, ElevenLabs, Google Translate, and PlaceHolder`s modules that will keep the system from crashing if you want to disable any of the modules.

[*CharacterAI*](https://beta.character.ai/) - Service for communicating with neural network - characters in private rooms!

[*Elevenlabs*](https://elevenlabs.io/) -  Service providing the ability to voice text! 

**Addons Repository**

Addons may have their own repositories and can be downloaded in the ``Addon Settings --> Download Addon menu``

It will bend the addon repository to a folder.

Tested addons will be placed in the [Addon List](ADDON_LIST.MD)

**!!! You need to have [GIT installed](https://git-scm.com/downloads) to download addons**

### | Let`s  begin!

The main thing is to have a complete set of Python components:
- **Python 3.11** 
- Python-PIP
- Python-VENV

*Remark: If you are a Windows user, you already have the full Python package. 
Linux users should check their system for these components*

[How to download or install a particular repository](https://docs.github.com/en/repositories/working-with-files/using-files/downloading-source-code-archives)

Let me remind you, this is not an application, just a kernel with a menu built into it

To customize the kernel modules you are going to use go to Settings 
By default, they should look like this:

```
[1] | Input method : Keybord Input
[2] | Translator of your text : GoogleTranslater
[3] | AI dialog : CharacterAI Chat
[4] | AI Text Translator : GoogleTranslater
[5] | Voice Method : ElevenLabs Voice
[6] | Conversation Language : ru.yml
```

(If not, you can kill any conterbuter of your choice)

The settings of individual modules are located in the **``Addon Settings``** menu

1. [Settings CharacterAI](addons/CharacterAI/README_RU.MD)
2. [Settings ElevenLabs](addons/ElevenLabs/README_RU.MD)
3. Quit, Quit, Start.

## For addon developers

The core has [documentation](docs/en/1.Components.MD) for questions [can be contacted](https://gulysh.art).

To publish the addon, you can commit.