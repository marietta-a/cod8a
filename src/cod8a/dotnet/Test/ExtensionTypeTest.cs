using System;
using System.IO;
using System.Linq;
using Xunit;
using CodeAnalyzer.Parsers;
using CodeAnalyzer.Models;

namespace MermaidTests.Mermaid
{
    public class ExtensionTypeTest
    {
        [Fact]
        public void Parse_ExtensionType_HandlesEmptyIdentifier()
        {
            // Arrange
            var testCode = @"
            namespace TestNamespace
            {
                extension(Color)
                {
                    public static Color GreenSmile()
                    {
                        return Color.FromArgb(83, 255, 26);
                    }
                }
            }";

            var filePath = Path.GetTempFileName() + ".cs";
            File.WriteAllText(filePath, testCode);

            try
            {
                var parser = new FileParser<FileStructure>
                {
                    FilePath = filePath,
                    Name = Path.GetFileName(filePath)
                };

                // Act
                var result = parser.Parse();

                // Assert
                Assert.NotNull(result);
                Assert.Single(result.Classes);
                var extensionClass = result.Classes.First();
                
                // This is what the user says is happening: it's empty.
                // We want it to NOT be empty, or at least handle it gracefully.
                Assert.Equal("extension(Color)", extensionClass.Name);

                // Verify Relationship
                Assert.NotNull(extensionClass.Relationships);
                Assert.Single(extensionClass.Relationships);
                var rel = extensionClass.Relationships.First();
                Assert.Equal("Extension", rel.Type);
                Assert.Equal("Color", rel.AssociatedItem);
            }
            finally
            {
                if (File.Exists(filePath)) File.Delete(filePath);
            }
        }
    }
}
