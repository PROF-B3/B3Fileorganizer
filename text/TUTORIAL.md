# B3FileOrganizer Tutorial - Complete Setup & Usage Guide

> **This tutorial will guide you through setting up and using B3FileOrganizer v2.0.0**

---

## 📋 Prerequisites

Before starting, ensure you have:
- **Windows 10/11, macOS, or Linux**
- **8GB+ RAM** (16GB+ recommended)
- **10GB+ free disk space**
- **Basic command line knowledge**

---

## 🚀 Installation Guide

### Step 1: Install Python
1. Go to [python.org](https://python.org)
2. Download Python 3.11 or newer
3. **IMPORTANT**: Check "Add Python to PATH" during installation
4. Verify installation: `python --version`

### Step 2: Install Ollama
1. Go to [ollama.ai](https://ollama.ai)
2. Download for your operating system
3. Install and start Ollama
4. Verify installation: `ollama --version`

### Step 3: Download AI Models
Open a terminal/command prompt and run:
```bash
ollama pull mixtral:latest
ollama pull llama3.2:3b
ollama pull codellama:latest
```

**Note**: This will download ~35GB of models. The download may take 30-60 minutes depending on your internet speed.

### Step 4: Install Project Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Verify Installation
```bash
python run_organize.py
```

You should see the main menu with 7 options.

---

## 🎯 First Steps

### Understanding the System
B3FileOrganizer uses four Greek AI agents:
- **Alpha (Α)**: Chief organizer and strategist
- **Beta (Β)**: Content analyzer and classifier
- **Gamma (Γ)**: Knowledge manager and Zettelkasten expert
- **Delta (Δ)**: Coordinator and workflow manager

### Basic Usage
1. **Start the system**: `python run_organize.py`
2. **Choose option 1**: Simple conversation with Alpha
3. **Ask questions** about file organization, Zettelkasten, or general topics
4. **Explore other options** to understand the system's capabilities

---

## 📚 Understanding the X and B Partitions

### The X Partition (Zettelkasten System)
The X partition is the heart of your knowledge organization:

```
X/
├── 1/           # Main topics (numbered)
├── 2/           # Further main topics
├── A/            # Frequently used topics
├── Z/            # Quotes and excerpts
└── _metadata/    # System metadata
    ├── card_index.json
    └── numbering_scheme.json
```

**How it works:**
- Each card gets a unique number based on content and category
- Cards are linked through references and tags
- The system automatically organizes knowledge using Luhmann's method
- You can search and browse your knowledge network

### The B Partition (Databases)
The B partition contains all system data:

```
databases/
├── b3team.db           # Main system database
├── conversations.db    # AI conversation history
└── wikipedia/          # Processed Wikipedia data
```

**Important**: Always backup these directories before major changes!

---

## 🔧 Advanced Usage

### Option 1: Simple Conversation
Perfect for learning and getting help:
- Ask about file organization strategies
- Get explanations of Zettelkasten concepts
- Discuss AI agent roles and capabilities

### Option 2: System Dashboard
Monitor your system's health:
- Check AI model availability
- View resource usage (CPU, RAM, disk)
- See system statistics and recent activity

### Option 3: Multi-Agent Organization
The full power of the system:
1. **Alpha** analyzes your files and suggests organization
2. **Beta** examines content and categorizes
3. **Gamma** creates Zettelkasten cards for knowledge
4. **Delta** coordinates the entire process

### Option 4: Wikipedia Knowledge Extraction
Process Wikipedia dumps into structured knowledge:
1. Download a Wikipedia dump file
2. Use the system to extract articles
3. Create Zettelkasten cards automatically
4. Build your personal knowledge base

### Option 5: Advanced File Analysis
Get detailed insights about individual files:
- Content analysis and categorization
- AI-generated insights and suggestions
- Organization recommendations

### Option 6: Learning System
The system learns from your usage:
- Analyzes patterns in your organization
- Suggests improvements
- Adapts to your preferences over time

### Option 7: Diagnostics
Comprehensive system health check:
- Tests all components
- Verifies AI model availability
- Checks database integrity
- Reports any issues

---

## 🛠️ Configuration

### Agent Configuration
Edit `config/agent_orchestrator.json` to customize agent behavior:
```json
{
  "agents": {
    "alpha": {
      "name": "Alpha",
      "greek_symbol": "Α",
      "role": "File Organization Specialist",
      "model": "mixtral:latest"
    }
  }
}
```

### AI Model Configuration
Edit `config/ai_models.json` to change model assignments:
```json
{
  "models": {
    "mixtral": {
      "name": "mixtral:latest",
      "description": "Main model for complex tasks"
    }
  }
}
```

---

## 📊 Working with Your Data

### Backing Up Your System
**Always backup before major changes:**
```bash
# Backup databases
cp -r databases/ databases_backup/

# Backup Zettelkasten
cp -r X/ X_backup/

# Full project backup
cp -r B3FileOrganizer/ B3FileOrganizer_backup/
```

### Understanding the Data Structure
- **b3team.db**: Contains organization history, learning patterns, agent interactions
- **conversations.db**: Stores all AI conversations for learning
- **X/**: Your personal knowledge network using Zettelkasten method

### Data Migration
If you need to move your system:
1. Stop the application
2. Copy the entire project folder
3. Copy your databases and X folder
4. Restart on the new system

---

## 🔍 Troubleshooting

### Common Issues

**"Ollama not found"**
```bash
# Check if Ollama is running
ollama --version

# Start Ollama if needed
ollama serve
```

**"AI models not available"**
```bash
# Check available models
ollama list

# Download missing models
ollama pull mixtral:latest
```

**"Python errors"**
```bash
# Check Python version
python --version

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**"Database errors"**
- The system creates databases automatically
- Check file permissions in the project directory
- Ensure you have write access

### Performance Issues

**High RAM usage:**
- AI models use significant memory
- Close other applications when running
- Consider using smaller models for testing

**Slow response times:**
- First run is slower as models load
- Subsequent runs are faster
- Consider using GPU acceleration if available

---

## 🎓 Advanced Features

### Custom Zettelkasten Workflows
1. **Create custom categories** in the X partition
2. **Link related cards** using the numbering system
3. **Build knowledge networks** around your interests
4. **Export and share** your knowledge structure

### Wikipedia Integration
1. **Download Wikipedia dumps** from Wikimedia
2. **Process articles** into structured knowledge
3. **Create Zettelkasten cards** automatically
4. **Build comprehensive knowledge bases**

### Multi-Agent Coordination
1. **Customize agent roles** in configuration
2. **Create specialized workflows** for your needs
3. **Monitor agent interactions** in the database
4. **Optimize performance** based on usage patterns

---

## 📈 Best Practices

### File Organization
- **Start small**: Organize a few files first
- **Use consistent naming**: Help the AI understand your patterns
- **Review suggestions**: The AI learns from your feedback
- **Backup regularly**: Protect your organized data

### Knowledge Management
- **Create meaningful card titles**: Help with searching and linking
- **Use tags consistently**: Enable better categorization
- **Link related cards**: Build your knowledge network
- **Review and refine**: Continuously improve your system

### System Maintenance
- **Monitor resource usage**: Ensure adequate RAM and disk space
- **Update AI models**: Keep models current for best performance
- **Backup regularly**: Protect your data and configurations
- **Test new features**: Verify changes before production use

---

## 🚀 Next Steps

### Learning Resources
- **Zettelkasten Method**: Study Niklas Luhmann's approach
- **AI Agent Systems**: Learn about multi-agent coordination
- **File Organization**: Explore different organizational systems
- **Knowledge Management**: Understand information architecture

### Community and Support
- **GitHub Issues**: Report bugs and request features
- **Documentation**: Read the detailed documentation files
- **Testing**: Run the test suite to verify your installation
- **Contributing**: Consider contributing to the project

### Advanced Development
- **Custom Agents**: Create specialized AI agents
- **Integration**: Connect with other tools and systems
- **Scaling**: Adapt the system for larger datasets
- **Deployment**: Set up for production environments

---

## 📞 Getting Help

If you encounter issues:
1. **Check the troubleshooting section** above
2. **Run diagnostics** (Option 7 in the main menu)
3. **Review the logs** in the project directory
4. **Check system requirements** and ensure adequate resources
5. **Search existing issues** on the project repository

---

*"The future of file organization is here. Thanks to Prof. B3 and his temporal transfer from the year 2073."*

**Happy organizing! 🚀** 