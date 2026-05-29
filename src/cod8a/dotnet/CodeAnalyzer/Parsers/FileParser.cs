using CodeAnalyzer.Models;
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

        public override required string Name { get; init; }

        /// <summary>
        /// Gets the code associated with this instance.
        /// </summary>
        public required string FilePath { get; init; }
        public int Id { get; init; } = 1;
        public override T Parse()
        {
            try
            {
                var code = File.ReadAllText(FilePath);
                // Parse the code into a SyntaxTree
                SyntaxTree tree = CSharpSyntaxTree.ParseText(code);

                // Get the root node of the tree
                CompilationUnitSyntax root = tree.GetCompilationUnitRoot();


                var fileName = Name ?? Path.GetFileName(FilePath);
                var id = 0;
                var usings = root.Usings.Select(b =>
                {
                    var name = GetName(b.Name);
                    return new UsingDirective(++id, name);
                });
                var fileStructure = new FileStructure
                {
                    Id = Id,
                    Name = fileName,
                    UsingDirectives = usings.ToList(),
                };


                fileStructure.Classes = GetClassDeclaration(root);

                return (T)fileStructure;
            }
            catch 
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
            catch
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

                foreach (var classDeclaration in typeDeclarationSyntaxes)
                {
                    var methodStructures = new List<MethodStructure>();
                    var parameterStructures = new List<ParameterStructure>();
                    var fieldStructures = new List<FieldStructure>();

                    var relationships = new List<RelationShip>();

                    var baseTypes = classDeclaration.BaseList?.Types;
                    int relId = 0;
                    int fieldId = 0;
                    int methodId = 0;
                    int classId = 0;

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
                                return new RelationShip (++relId, type, parent);
                            })
                        );
                    }

                    // Extract standard fields and properties
                    fieldStructures.AddRange(classDeclaration.DescendantNodes().OfType<FieldDeclarationSyntax>().Select(f => new FieldStructure(++fieldId, f.Declaration.Variables.First().Identifier.Text, f.Modifiers.ToFullString().Trim(), f.Declaration.Type.ToString(), f.GetLeadingTrivia().ToString().Trim())));
                    fieldStructures.AddRange(classDeclaration.DescendantNodes().OfType<PropertyDeclarationSyntax>().Select(f => new FieldStructure(++fieldId, f.Identifier.Text, f.Modifiers.ToFullString().Trim(), f.Type.ToString(), f.GetLeadingTrivia().ToString().Trim())));
                    
                    // Extract record positional parameters as properties
                    if (classDeclaration is RecordDeclarationSyntax recordDecl && recordDecl.ParameterList != null)
                    {
                        fieldStructures.AddRange(recordDecl.ParameterList.Parameters.Select(p => new FieldStructure(++fieldId, p.Identifier.Text, "public", p.Type?.ToString() ?? "", p.GetLeadingTrivia().ToString().Trim())));
                    }

                    foreach (var method in classDeclaration.Members.OfType<MethodDeclarationSyntax>())
                    {
                        var parameters = method.ParameterList.Parameters.Select(p => new ParameterStructure(p.Identifier.Text, p.Modifiers.ToFullString().Trim(), p.Type?.ToString() ?? "", p.GetLeadingTrivia().ToString().Trim())).ToList();
                        parameterStructures.AddRange(parameters);

                        methodStructures.Add(new MethodStructure(++methodId, method.Identifier.Text, method.Modifiers.ToFullString().Trim(), method.ReturnType.ToString(), parameters, method.GetLeadingTrivia().ToString().Trim()));
                    }

                    var className = classDeclaration.Identifier.Text;
                    if (string.IsNullOrEmpty(className) && classDeclaration.Keyword.Text == "extension")
                    {
                        var parameterList = classDeclaration.ChildNodes().OfType<ParameterListSyntax>().FirstOrDefault();
                        if (parameterList != null && parameterList.Parameters.Any())
                        {
                            var extendedType = parameterList.Parameters[0].Type;
                            if (extendedType != null)
                            {
                                className = $"{extendedType}ExtensionBlock";
                                relationships.Add(new RelationShip(++relId, "Extension", extendedType.ToString()));
                            }
                        }
                        else
                        {
                            className = "extension";
                        }
                    }

                    classes.Add(new ClassStructure(++classId, className, methodStructures, fieldStructures, classDeclaration.Keyword.ToFullString().Trim(), relationships, classDeclaration.GetLeadingTrivia().ToString().Trim()));
                }

                return classes;
            }
            catch
            {
                throw;
            }
        }
    }
}


