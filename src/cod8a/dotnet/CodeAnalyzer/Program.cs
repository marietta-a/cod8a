using System;
using System.IO;
using System.Linq;
using System.Text.Json;
using CodeAnalyzer.Models;
using CodeAnalyzer.Parsers;

class Program
{
    static void Main(string[] args)
    {
        var path = args.Length > 0 ? args[0] : null;

        if(string.IsNullOrEmpty(path))
        {
            Console.Error.WriteLine(@"No file or project specified. Please provide a file/directory
                                     containing ...cs, .csproj, or .sln file.");
            return;
        }

        //Check if path is directory
        var fileAttr = File.GetAttributes(path!);
        var isDirectory = fileAttr.HasFlag(FileAttributes.Directory);


        if (!File.Exists(path) && !isDirectory){
            Console.Error.WriteLine($"File not found: {path}");
            return;
        }
        
        var json = "";
        var fileName = Path.GetFileName(path);

        if (isDirectory || path.EndsWith(".csproj") || path.EndsWith(".sln") || path.EndsWith(".slnx"))
        {
            var directoryPath = isDirectory ? path : Path.GetDirectoryName(path)!;
            var csFiles = Directory.GetFiles(directoryPath, "*.cs", SearchOption.TopDirectoryOnly).Where(f => !f.Contains("obj", StringComparison.CurrentCultureIgnoreCase)).ToArray();

            BaseParser<ProjectStructure> projectStructure = new ProjectParser<ProjectStructure>()
            {
                FilePaths = csFiles,
                Name = fileName,
            };

            json = JsonSerializer.Serialize(projectStructure.Parse(), new JsonSerializerOptions { WriteIndented = false });
        }
        else
        {
            BaseParser<FileStructure> fileStructure = new FileParser<FileStructure>()
            {
                FilePath = path,
                Name = fileName,
            };

            json = JsonSerializer.Serialize(fileStructure.Parse(), new JsonSerializerOptions { WriteIndented = false });
        }

        Console.WriteLine(json);

    }
}
