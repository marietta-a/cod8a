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
        string projectRoot = args.Length > 0 ? args[0] : Directory.GetCurrentDirectory();
        string fileName = args.Length > 1 ? args[1] : null;
        var arr = projectRoot.Split("\\");
        projectRoot = string.Join("\\", arr.Take(arr.Length - 3));

        if (!Directory.Exists(projectRoot))
        {
            Console.Error.WriteLine($"Project root not found: {projectRoot}");
            return;
        }

        var csFiles = Directory.GetFiles(projectRoot, "*.cs", SearchOption.AllDirectories);
        csFiles = csFiles.Where(b => !b.Contains("obj", StringComparison.CurrentCultureIgnoreCase)).ToArray();

        string json = "";

        if (!string.IsNullOrEmpty(fileName))
        {
            var existingFilePath = csFiles.FirstOrDefault(f => Path.GetFileName(f).Contains(fileName, StringComparison.CurrentCultureIgnoreCase));
            if (string.IsNullOrEmpty(existingFilePath))
            {
                Console.Error.WriteLine("File not found");
                return;
            }

            BaseParser<FileStructure> fileStructure = new FileParser<FileStructure>()
            {
                FilePath = existingFilePath,
                Name = Path.GetFileName(existingFilePath),
            };

            json = JsonSerializer.Serialize(fileStructure.Parse(), new JsonSerializerOptions { WriteIndented = false });
        }
        else
        {
            BaseParser<ProjectStructure> projectStructure = new ProjectParser<ProjectStructure>()
            {
                FilePaths = csFiles,
                Name = Path.GetFileName(projectRoot),
            };

            json = JsonSerializer.Serialize(projectStructure.Parse(), new JsonSerializerOptions { WriteIndented = false });
        }

        Console.WriteLine(json);
    }
}
