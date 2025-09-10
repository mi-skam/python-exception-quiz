# Python Exception Quiz - itch.io Deployment Guide

This guide covers deploying your pygame-based Python Exception Quiz to itch.io in two formats:
- **Desktop Executable** (downloadable)
- **Web Game** (browser-playable)

## Prerequisites

- Python 3.8+
- All game dependencies installed (`pygame`, etc.)
- itch.io account

## Method 1: Desktop Executable Deployment

### Step 1: Build the Executable

Run the build script:

```bash
python build_executable.py --package
```

This will:
- Install PyInstaller if needed
- Create a single executable file
- Package it with assets in `dist/PythonExceptionQuiz_Package/`

### Step 2: Upload to itch.io

1. **Create New Project** on itch.io
2. **Upload Files:**
   - Zip the contents of `dist/PythonExceptionQuiz_Package/`
   - Upload the zip file
3. **Configure:**
   - Kind of project: **Game**
   - Platforms: Check **Windows**, **macOS**, **Linux** (as appropriate)
   - Classification: **Downloadable**
   - Pricing: Set as desired (can be free)

### Step 3: Test

- Download and test on your target platforms
- Verify the executable runs without requiring Python installation

## Method 2: Web Game Deployment

### Step 1: Build the Web Version

Run the web build script:

```bash
python build_web.py --package
```

This will:
- Install pygbag if needed
- Convert pygame code to web-compatible format
- Create browser-ready files in `itch_web_package/`

### Step 2: Upload to itch.io

1. **Create New Project** on itch.io
2. **Upload Files:**
   - Zip the contents of `itch_web_package/`
   - Upload the zip file
3. **Configure:**
   - Kind of project: **Game**
   - Platforms: Check **HTML5**
   - Classification: **HTML**
   - **Embed options:**
     - Viewport dimensions: **800 x 600** (or larger)
     - Fullscreen button: **Yes**
     - Mobile friendly: **No** (pygame games work best on desktop)

### Step 3: Set Main File

- In the uploads section, mark `index.html` as **"This file will be played in the browser"**

## Troubleshooting

### Desktop Build Issues

**"ModuleNotFoundError" when running executable:**
- Ensure all dependencies are in the same directory
- Check that data files are included in the package

**Large file size:**
- This is normal for PyInstaller builds
- Consider using `--onedir` instead of `--onefile` for smaller individual files

### Web Build Issues

**"pygbag not working" or import errors:**
```bash
pip install --upgrade pygbag
```

**Game not loading in browser:**
- Check browser console for errors
- Ensure all assets are web-compatible
- Test locally before uploading

**Performance issues:**
- Web version may run slower than desktop
- Consider reducing screen size or game complexity for web

### General itch.io Issues

**Game not appearing after upload:**
- Check that files are properly unzipped on itch.io
- Verify the main executable/HTML file is marked correctly

**Players can't run the game:**
- For desktop: Include clear system requirements
- For web: Test in multiple browsers (Chrome, Firefox, Safari)

## File Structure Reference

After building, your project should have:

```
python-exception-quiz/
├── build_executable.py          # Desktop build script
├── build_web.py                 # Web build script  
├── pygame_web.py               # Async-compatible pygame code
├── dist/                       # Desktop build output
│   └── PythonExceptionQuiz_Package/
├── dist_web/                   # Raw web build files
└── itch_web_package/           # Ready-to-upload web package
```

## Deployment Checklist

### Desktop Version
- [ ] Game builds without errors
- [ ] Executable runs on target platforms  
- [ ] All assets are included
- [ ] README.txt is clear and helpful
- [ ] itch.io project configured for downloads
- [ ] Tested download and installation

### Web Version
- [ ] Pygame code is async-compatible
- [ ] Web build completes successfully
- [ ] Game loads and runs in browser
- [ ] All controls work (keyboard, mouse)
- [ ] itch.io project configured for HTML5
- [ ] index.html marked as main file
- [ ] Tested in multiple browsers

## Tips for Success

1. **Start Simple:** Get basic deployment working before adding complex features
2. **Test Early:** Upload and test on itch.io before finalizing
3. **Include Instructions:** Clear gameplay instructions help player engagement
4. **Screenshot/GIFs:** Add attractive media to your itch.io page
5. **Both Versions:** Consider offering both desktop and web versions

## Support

If you encounter issues:
1. Check the error messages carefully
2. Ensure all dependencies are correctly installed
3. Test builds locally before uploading
4. itch.io has extensive documentation for HTML5 games

---

Good luck with your deployment! 🎮🐍