using CodeAnalyzer.models;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;
using Microsoft.CodeAnalysis.CSharp.Syntax;
using System;
using System.Collections.Generic;
using System.Text;
using System.Text.Json;

namespace CodeAnalyzer.Parsers
{
    /// <summary>
    /// Provides functionality to parse C# source code files and extract their structural information, such as using
    /// directives and class definitions.
    /// </summary>
    /// <remarks>Use this class to analyze the contents of a C# file by supplying its code and file name. The
    /// parser returns a structured representation of the file, which includes details about its using directives and
    /// classes. This class is not thread-safe.</remarks>
    public sealed partial class FileParser<T> : BaseParser<T> where T : FileStructure
    {

        public override string Name { get; init; }

        /// <summary>
        /// Gets the code associated with this instance.
        /// </summary>
        public string FilePath { get; init; }
        public override T Parse()
        {
            try
            {
                var code = File.ReadAllText(FilePath);
                // Parse the code into a SyntaxTree
                SyntaxTree tree = CSharpSyntaxTree.ParseText(code);

                // Get the root node of the tree
                CompilationUnitSyntax root = tree.GetCompilationUnitRoot();


                var directory = Directory.GetCurrentDirectory();
                var fileName = Path.GetFileName(directory);
                var id = 0;
                var usings = root.Usings.Select(b =>
                {
                    var name = GetName(b.Name);
                    return new UsingDirective(++id, name);
                });
                var fileStructure = new FileStructure
                {
                    Id = 1,
                    Name = fileName,
                    UsingDirectives = usings.ToList(),
                };


                fileStructure.Classes = GetClassDeclaration(root);

                return (T)fileStructure;
            }
            catch (Exception ex)
            {
                throw;
            }
        }

        private string GetName(NameSyntax? nameSyntax)
        {
            try
            {
                return nameSyntax switch
                {
                    null => string.Empty,
                    SimpleNameSyntax simpleName => simpleName.Identifier.Text,
                    QualifiedNameSyntax qualifiedName => qualifiedName.Right.Identifier.Text,
                    AliasQualifiedNameSyntax aliasQualifiedName => aliasQualifiedName.Name.Identifier.Text,
                    _ => string.Empty
                };
            }
            catch( Exception ex )
            {
                throw;
            }
        }

        private List<ClassStructure> GetClassDeclaration(CompilationUnitSyntax root)
        {
            var classes = new List<ClassStructure>();
            try
            {
                var typeDeclarationSyntaxes = root.DescendantNodes().OfType<TypeDeclarationSyntax>();
                var fieldStructures = new List<FieldStructure>();

                foreach (var classDeclaration in typeDeclarationSyntaxes)
                {
                    var methodStructures = new List<MethodStructure>();
                    var parameterStructures = new List<ParameterStructure>();

                    var relationships = new List<RelationShip>();

                    var baseTypes = classDeclaration.BaseList?.Types;
                    int id = 0;

                    if(baseTypes is not null)
                    {
                        
                        relationships.AddRange(
                            baseTypes.Value.Select(b => {
                                string parent = b.Type switch
                                {
                                    SimpleNameSyntax simpleName => simpleName.Identifier.Text,
                                    QualifiedNameSyntax qualifiedName => qualifiedName.Right.Identifier.Text,
                                    _ => b.Type.ToString().Split('<')[0]
                                };
                                var type = parent.StartsWith("I") && parent.Length > 1 && char.IsUpper(parent[1]) ? "Interface" : "Class";
                                return new RelationShip (++id, type, parent);
                            })
                        );
                    }


                    fieldStructures.AddRange(classDeclaration.DescendantNodes().OfType<FieldDeclarationSyntax>().Select(f => new FieldStructure(default, f.Declaration.Variables.First().Identifier.Text, f.Modifiers.ToFullString().Trim(), f.Declaration.Type.ToString(), f.GetLeadingTrivia().ToString().Trim())));
                    fieldStructures.AddRange(classDeclaration.DescendantNodes().OfType<PropertyDeclarationSyntax>().Select(f => new FieldStructure(default, f.Identifier.Text, f.Modifiers.ToFullString().Trim(), f.Type.ToString(), f.GetLeadingTrivia().ToString().Trim())));
                    foreach (var method in classDeclaration.Members.OfType<MethodDeclarationSyntax>())
                    {
                        var parameters = method.ParameterList.Parameters.Select(p => new ParameterStructure(p.Identifier.Text, p.Modifiers.ToFullString().Trim(), p.Type.ToString(), p.GetLeadingTrivia().ToString().Trim())).ToList();
                        parameterStructures.AddRange(parameters);

                        methodStructures.Add(new MethodStructure(default, method.Identifier.Text, method.Modifiers.ToFullString().Trim(), method.ReturnType.ToString(), parameters, method.GetLeadingTrivia().ToString().Trim()));
                    }
                    classes.Add(new ClassStructure(default, classDeclaration.Identifier.Text, methodStructures, fieldStructures, classDeclaration.Keyword.ToFullString().Trim(), relationships, classDeclaration.GetLeadingTrivia().ToString().Trim()));
                }

                return classes;
            }
            catch (Exception ex)
            {
                throw;
            }
        }
    }
}

