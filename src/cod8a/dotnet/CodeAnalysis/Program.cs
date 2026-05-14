using System;
using System.IO;
using System.Linq;
using System.Text.Json;
using CodeAnalyzer.models;
using CodeAnalyzer.Parsers;

class Program
{
    static void Main(string[] args)
    {
        Console.WriteLine("Starting code analysis...");
        var fileName = args.Length > 0 ? args[0] : null;


        if(string.IsNullOrEmpty(fileName))
        {
            Console.Error.WriteLine("No file or project specified. Please provide a .cs, .csproj, or .sln file.");
            return;
        }

        if (!File.Exists(fileName)){
            Console.Error.WriteLine($"File not found: {fileName}");
            return;
        }
        
        string json = "";

        if(fileName.EndsWith(".csproj", StringComparison.CurrentCultureIgnoreCase) || fileName.EndsWith(".sln", StringComparison.CurrentCultureIgnoreCase))
        {
            var csFiles = Directory.GetFiles(Path.GetDirectoryName(fileName)!, "*.cs", SearchOption.AllDirectories).Where(f => !f.Contains("obj", StringComparison.CurrentCultureIgnoreCase)).ToArray();

            BaseParser<ProjectStructure> projectStructure = new ProjectParser<ProjectStructure>()
            {
                FilePaths = csFiles,
                Name = Path.GetFileName(fileName),
            };

            json = JsonSerializer.Serialize(projectStructure.Parse(), new JsonSerializerOptions { WriteIndented = false });
        }
        else
        {
            BaseParser<FileStructure> fileStructure = new FileParser<FileStructure>()
            {
                FilePath = fileName,
                Name = Path.GetFileName(fileName),
            };

            json = JsonSerializer.Serialize(fileStructure.Parse(), new JsonSerializerOptions { WriteIndented = false });
        }

        Console.WriteLine(json);
    }
}
