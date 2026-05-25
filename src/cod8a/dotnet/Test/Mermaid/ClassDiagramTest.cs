using System;
using System.IO;
using System.Linq;
using Xunit;
using CodeAnalyzer.Parsers;
using CodeAnalyzer.Models;

namespace MermaidTests.Mermaid
{
    public class ClassDiagramTest
    {
        [Fact]
        public void Parse_GeneratesCorrectRelationshipsForMermaid()
        {
            // Arrange
            var testCode = @"
            namespace TestNamespace
            {
                public interface IEmployee { }

                public class Employee : IEmployee
                {
                    public string Name { get; set; }
                }

                public class Manager
                {
                    public Employee Employee;
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

                var employeeClass = result.Classes.First(c => c.Name == "Employee");
                var managerClass = result.Classes.First(c => c.Name == "Manager");

                // Test Inheritance/Interface Relationship (Mermaid uses this for <|-- and <|..)
                Assert.Single(employeeClass.Relationships);
                var interfaceRel = employeeClass.Relationships.First();
                Assert.Equal("Interface", interfaceRel.Type);
                Assert.Equal("IEmployee", interfaceRel.AssociatedItem);

                // Test Composition/Uses Relationship (Mermaid uses this for --> contains/uses)
                Assert.Single(managerClass.Fields);
                var employeeField = managerClass.Fields.First();
                Assert.Equal("Employee", employeeField.Type);
                Assert.Equal("Employee", employeeField.Name);
            }
            finally
            {
                File.Delete(filePath);
            }
        }
    }
}

