using System;
using System.Collections.Generic;
using System.Text;

namespace CodeAnalyzer.models
{
    public class ProjectStructure
    {
        /// <summary>
        /// Id of the Project
        /// </summary>
        public int Id { get; set; }

        /// <summary>
        /// Name of the Project
        /// </summary>
        public string Name { get; set; }

        /// <summary>
        /// Project Description
        /// </summary>
        public string Description { get; set; }

        /// <summary>
        /// Gets or sets the collection of files associated with the Project.
        /// </summary>
        public List<FileStructure> Files { get; set; }
    }
}
