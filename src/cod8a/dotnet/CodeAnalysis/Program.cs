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
        //Check if path is directory
        var fileAttr = File.GetAttributes(fileName!);
        var isDirectory = fileAttr.HasFlag(FileAttributes.Directory);


        if(string.IsNullOrEmpty(fileName))
        {
            Console.Error.WriteLine(@"No file or project specified. Please provide a file/directory
                                     containing ...cs, .csproj, or .sln file.");
            return;
        }

        if (!File.Exists(fileName) && !isDirectory){
            Console.Error.WriteLine($"File not found: {fileName}");
            return;
        }
        
        string json = "";

        if (isDirectory || fileName.EndsWith(".csproj") || fileName.EndsWith(".sln") || fileName.EndsWith(".slnx"))
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
